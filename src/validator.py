import os
import yaml
import json
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional

from src.connector.db_connector import DBConnector
from src.infrastructure.integrity import IntegrityChecker
from src.infrastructure.tracker import ExecutionTracker
from src.infrastructure.watermark import WatermarkManager

# Reutilizamos ConfigLoader de builder si es necesario, 
# pero aquí necesitamos uno más específico para la Phase 2.1
from src.builder import ConfigLoader

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ContractValidator")

class ContractValidator:
    """
    Motor Principal de Validación de Contratos de Datos (Gatekeeper).
    Orquesta la seguridad, sincronización y calidad de los datos.
    [ARC-12]
    """

    def __init__(self, phase: str = "validation_mvp"):
        self.phase_key = phase
        self.config_loader = ConfigLoader()
        self.config = self.config_loader.config.get(self.phase_key, {})
        
        if not self.config:
            raise ValueError(f"No se encontró configuración para la fase: {phase}")

        self.db = DBConnector()
        self.tracker = ExecutionTracker()
        self.watermark_mgr = WatermarkManager()
        
        # El contrato físico se busca en la ruta definida en storage/artifacts dentro de builder
        # Pero para el MVP, asumimos la ruta estándar
        storage = self.config_loader.config.get("storage", {})
        contracts_dir = storage.get("local", {}).get("contracts_dir", "contract")
        contract_file = storage.get("artifacts", {}).get("data_contract_file", "data_contract.yaml")
        self.contract_path = os.path.join(contracts_dir, contract_file)
        
        self.integrity_checker = IntegrityChecker(self.contract_path)
        
        self.target_table = self.config.get("target_table")
        self.time_column = self.config.get("time_column")
        self.severities = self.config.get("severities", {})

    def validate_gate(self, df: pd.DataFrame) -> bool:
        """
        Ejecuta el flujo completo de validación (Gatekeeper).
        Retorna True si la validación es exitosa o aceptable (WARNING), False si falla (FAILED).
        """
        logger.info(f"🛡️ Iniciando Gatekeeper para tabla: {self.target_table}")
        start_time = datetime.now()
        
        local_report_path = self.config.get("operational_paths", {}).get("local_report", "docs/validation/report.json")
        
        # 1. INTEGRITY CHECK [REQ-HAS-01]
        integrity = self.integrity_checker.verify_integrity(self.target_table)
        contract_id = integrity.get("contract_id")
        
        # 4. AUDIT INIT (Lo adelantamos para capturar fallos tempranos)
        self.tracker.start_pipeline_execution(
            phase=self.phase_key,
            mode="LOAD",
            contract_id=contract_id if contract_id else None,
            watermark_start=None
        )

        if not integrity["success"]:
            error_msg = f"SECURITY_BREACH: {integrity.get('error')}"
            logger.error(f"❌ FALLO DE INTEGRIDAD: {error_msg}")
            
            # Persistencia de fallo de integridad
            latency = int((datetime.now() - start_time).total_seconds() * 1000)
            self.tracker.log_validation_details(
                table_name=self.target_table,
                status="FAILED",
                details={"security": {"status": "FAILED", "errors": [error_msg]}},
                latency_ms=latency
            )
            self.tracker.end_pipeline_execution(
                status="ABORTED",
                validation_status="FAILED",
                error_summary=error_msg
            )
            # Reporte Local
            self.tracker.generate_local_report(local_report_path, {
                "timestamp": datetime.now().isoformat(),
                "status": "FAILED",
                "reason": error_msg,
                "integrity": integrity
            })
            return False
        
        # 2. WATERMARK CHECK [REQ-WAT-01]
        last_watermark = self.watermark_mgr.get_last_successful_watermark(self.phase_key, contract_id)
        # Usamos updated_at para capturar tanto inserciones nuevas como ediciones en la historia
        current_max = self.watermark_mgr.get_current_max_date(self.target_table, "updated_at")
        
        sync_eval = self.watermark_mgr.evaluate_sync_type(last_watermark, current_max)
        logger.info(f"🔄 Modo de Sincronización: {sync_eval['type']} - {sync_eval['message']}")
        
        if sync_eval["type"] == "NO_NEW_DATA":
            logger.info("⏭️ No hay datos nuevos para validar. Saltando pipeline.")
            self.tracker.end_pipeline_execution(
                status="SKIPPED", 
                validation_status="SUCCESS", 
                watermark_end=current_max, 
                error_summary="No new data detected.",
                watermark_start=last_watermark,
                validation_type=sync_eval["type"]
            )
            self.tracker.generate_local_report(local_report_path, {
                "timestamp": datetime.now().isoformat(),
                "status": "SKIPPED",
                "reason": "No new data",
                "watermark": current_max.isoformat() if current_max else None
            })
            return True 

        # 3. LOAD CONTRACT RULES
        try:
            with open(self.contract_path, "r", encoding="utf-8") as f:
                full_contract = yaml.safe_load(f)
                sources = full_contract.get("sources", {})
                # Intentamos buscar por el alias/label definido en config.yaml
                source_label = next(
                    (s["name"] for s in self.config_loader.get_sources() if s["db_table"] == self.target_table),
                    self.target_table
                )
                table_rules = sources.get(source_label)
                
                if not table_rules:
                    raise ValueError(f"Reglas no encontradas para la fuente '{source_label}' (Tabla: {self.target_table})")
        except Exception as e:
            error_msg = f"Error al cargar reglas de contrato: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.tracker.end_pipeline_execution(
                status="ABORTED", 
                validation_status="FAILED", 
                error_summary=error_msg,
                watermark_start=last_watermark,
                validation_type=sync_eval["type"]
            )
            self.tracker.generate_local_report(local_report_path, {"status": "FAILED", "reason": error_msg})
            return False

        # 5. DATA VALIDATION (Core Logic)
        source_config = next(
            (s for s in self.config_loader.get_sources() if s["db_table"] == self.target_table),
            {}
        )
        frequency = source_config.get("frequency", "daily")
        
        results, global_status = self._run_core_validations(df, table_rules, frequency)
        
        # 6. PERSISTENCE & CLOSE [REQ-OUT-02]
        latency = int((datetime.now() - start_time).total_seconds() * 1000)
        self.tracker.log_validation_details(
            table_name=self.target_table,
            status=global_status,
            details=results,
            latency_ms=latency
        )
        
        self.tracker.end_pipeline_execution(
            status="COMPLETED" if global_status != "FAILED" else "ABORTED",
            validation_status=global_status,
            watermark_end=current_max,
            error_summary=None if global_status == "SUCCESS" else "Validación con hallazgos",
            metadata={"rows_processed": len(df), "latency_ms": latency},
            watermark_start=last_watermark,
            validation_type=sync_eval["type"]
        )

        # Reporte Local Final
        self.tracker.generate_local_report(local_report_path, {
            "timestamp": datetime.now().isoformat(),
            "status": global_status,
            "table": self.target_table,
            "results": results,
            "latency_ms": latency,
            "rows_processed": len(df)
        })

        return global_status != "FAILED"

    def _run_core_validations(self, df: pd.DataFrame, rules: dict, frequency: str) -> (dict, str):
        """
        Ejecuta las pruebas de Esquema, Duplicados, Centinelas, Continuidad y Reglas de Negocio.
        """
        logger.info(f"🧪 Ejecutando suite de validaciones core (Freq: {frequency})...")
        results = {}
        max_severity = "SUCCESS"
        thresholds = self.config_loader.config.get("thresholds", {})

        # A. Estructural: Columnas y Tipos [REQ-STR-01]
        expected_schema = rules.get("schema", {})
        val_config = rules.get("validations", {})
        structural_errors = []
        structural_tests = []
        
        # 1. Esquema y Tipado
        for col, expected_dtype in expected_schema.items():
            test_info = {"name": f"Schema check: {col}", "target": col, "expected": expected_dtype}
            if col not in df.columns:
                test_info["status"] = self.severities.get("structural", "FAILED")
                test_info["error"] = "Column missing"
                structural_errors.append(f"Columna faltante: {col}")
            else:
                actual_dtype = str(df[col].dtype)
                test_info["actual"] = actual_dtype
                # Simplificación de tipos para validación robusta
                match = ("int" in expected_dtype and "int" in actual_dtype) or \
                        ("float" in expected_dtype and "float" in actual_dtype) or \
                        ("object" in expected_dtype and actual_dtype == "object")
                
                if not match:
                    test_info["status"] = self.severities.get("structural", "FAILED")
                    test_info["error"] = f"Type mismatch: expected {expected_dtype}, got {actual_dtype}"
                    structural_errors.append(f"Tipo incorrecto en {col}: esperado {expected_dtype}, recibido {actual_dtype}")
                else:
                    test_info["status"] = "SUCCESS"
            structural_tests.append(test_info)

        # 2. Columnas Extras [REQ-STR-01]
        if not val_config.get("allow_extra_columns", False):
            extra_cols = [c for c in df.columns if c not in expected_schema and c not in ['created_at', 'updated_at']]
            test_info = {"name": "Extra columns check", "target": "dataframe", "status": "SUCCESS"}
            if extra_cols:
                # Filtrar created_at/updated_at si no están en schema pero están en df (común en Supabase)
                # Ya lo hice en la línea anterior
                if extra_cols:
                    test_info["status"] = self.severities.get("structural", "FAILED")
                    test_info["error"] = f"Found extra columns: {extra_cols}"
                    structural_errors.append(f"Columnas no declaradas: {extra_cols}")
            structural_tests.append(test_info)

        # 3. Columnas Duplicadas
        test_info = {"name": "Duplicate columns check", "target": "dataframe", "status": "SUCCESS"}
        if df.columns.duplicated().any():
            dup_cols = df.columns[df.columns.duplicated()].unique().tolist()
            test_info["status"] = self.severities.get("structural", "FAILED")
            test_info["error"] = f"Found duplicate column names: {dup_cols}"
            structural_errors.append(f"Nombres de columnas duplicados: {dup_cols}")
        structural_tests.append(test_info)

        status_str = "SUCCESS" if not structural_errors else self.severities.get("structural", "FAILED")
        results["structural"] = {"status": status_str, "errors": structural_errors, "tests": structural_tests}
        if status_str == "FAILED": max_severity = "FAILED"

        # B. Continuidad y Frescura (Time Boundary Logic) [REQ-WAT-01]
        continuity_errors = []
        continuity_tests = []
        
        if self.time_column in df.columns:
            # Asegurar que la columna es datetime
            df_dates = pd.to_datetime(df[self.time_column], errors='coerce').dropna()
            if not df_dates.empty:
                max_date = df_dates.max()
                today = pd.Timestamp.now()
                
                # 1. Regla de Oro / Frescura (X-1 / Boundary)
                if val_config.get("check_gold_rule") or val_config.get("check_freshness"):
                    leak_msg = ""
                    stale_msg = ""
                    
                    if frequency == "daily":
                        # X-1: La información debe ser exactamente el día anterior
                        limit_date = (today - pd.Timedelta(days=1)).normalize()
                        max_date_naive = max_date.replace(tzinfo=None).replace(hour=0, minute=0, second=0, microsecond=0)
                        limit_date_naive = limit_date.replace(tzinfo=None)
                        leak_msg = f"Data Leakage (Daily): Max date {max_date_naive.date()} is ahead of X-1 ({limit_date_naive.date()})"
                        stale_msg = f"Stale Data (Daily): Max date {max_date_naive.date()} is behind X-1 ({limit_date_naive.date()})"
                    
                    elif frequency == "monthly":
                        # Mes actual, excepto el día 1 que es el mes anterior
                        if today.day == 1:
                            limit_date = (today - pd.DateOffset(months=1)).replace(day=1).normalize()
                        else:
                            limit_date = today.replace(day=1).normalize()
                        
                        max_date_naive = max_date.replace(tzinfo=None).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                        limit_date_naive = limit_date.replace(tzinfo=None)
                        leak_msg = f"Data Leakage (Monthly): Max month {max_date_naive.strftime('%Y-%m')} is ahead of expected {limit_date_naive.strftime('%Y-%m')}"
                        stale_msg = f"Stale Data (Monthly): Max month {max_date_naive.strftime('%Y-%m')} is behind expected {limit_date_naive.strftime('%Y-%m')}"
                    
                    elif frequency == "annual" or frequency == "yearly":
                        # Año actual, excepto el 1 de enero que es el año anterior
                        if today.month == 1 and today.day == 1:
                            limit_date = (today - pd.DateOffset(years=1)).replace(month=1, day=1).normalize()
                        else:
                            limit_date = today.replace(month=1, day=1).normalize()
                        
                        max_date_naive = max_date.replace(tzinfo=None).replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                        limit_date_naive = limit_date.replace(tzinfo=None)
                        leak_msg = f"Data Leakage (Annual): Max year {max_date_naive.year} is ahead of expected {limit_date_naive.year}"
                        stale_msg = f"Stale Data (Annual): Max year {max_date_naive.year} is behind expected {limit_date_naive.year}"

                    # TEST 1: DATA LEAKAGE
                    leak_test = {"name": "Data Leakage check", "target": self.time_column, "max_date": str(max_date)}
                    if max_date_naive > limit_date_naive:
                        leak_test["status"] = self.severities.get("continuity", "FAILED")
                        leak_test["error"] = leak_msg
                        continuity_errors.append(leak_msg)
                    else:
                        leak_test["status"] = "SUCCESS"
                    continuity_tests.append(leak_test)

                    # TEST 2: STALE DATA
                    stale_test = {"name": "Stale Data check", "target": self.time_column, "max_date": str(max_date)}
                    if max_date_naive < limit_date_naive:
                        stale_test["status"] = self.severities.get("continuity", "FAILED")
                        stale_test["error"] = stale_msg
                        continuity_errors.append(stale_msg)
                    else:
                        stale_test["status"] = "SUCCESS"
                    continuity_tests.append(stale_test)

                # 2. Gaps (Continuidad temporal)
                if val_config.get("check_gaps") and frequency == "daily":
                    test_info = {"name": "Temporal gaps check", "target": self.time_column}
                    full_range = pd.date_range(start=df_dates.min(), end=df_dates.max(), freq='D')
                    missing = full_range.difference(df_dates.unique())
                    if not missing.empty:
                        test_info["status"] = self.severities.get("continuity", "FAILED")
                        test_info["missing_count"] = len(missing)
                        test_info["error"] = f"Found {len(missing)} missing dates. (Gaps)"
                        continuity_errors.append(f"Gaps detectados: {len(missing)} fechas faltantes.")
                    else:
                        test_info["status"] = "SUCCESS"
                    continuity_tests.append(test_info)

        status_cont = "SUCCESS" if not continuity_errors else self.severities.get("continuity", "FAILED")
        results["continuity"] = {"status": status_cont, "errors": continuity_errors, "tests": continuity_tests}
        if status_cont == "FAILED": max_severity = "FAILED"
        elif status_cont == "WARNING" and max_severity == "SUCCESS": max_severity = "WARNING"

        # C. Calidad: Nulos, Duplicados y Centinelas [REQ-VAL-01]
        quality_errors = []
        quality_tests = []
        
        # 1. Nulos
        null_counts = df.isnull().sum().to_dict()
        for col in df.columns:
            if not val_config.get("allow_nulls", False):
                count = int(null_counts.get(col, 0))
                test_info = {"name": f"Null check: {col}", "target": col, "null_count": count}
                if count > 0:
                    test_info["status"] = self.severities.get("quality", "WARNING")
                    test_info["error"] = f"Found {count} null values."
                    quality_errors.append(f"Columna {col} tiene {count} nulos.")
                else:
                    test_info["status"] = "SUCCESS"
                quality_tests.append(test_info)

        # 2. Duplicados
        if not val_config.get("allow_duplicates_rows", False):
            dup_count = int(df.duplicated().sum())
            test_info = {"name": "Duplicate rows check", "target": "dataframe", "dup_count": dup_count}
            if dup_count > 0:
                test_info["status"] = self.severities.get("quality", "WARNING")
                test_info["error"] = f"Found {dup_count} duplicate rows."
                quality_errors.append(f"Se encontraron {dup_count} filas duplicadas.")
            else:
                test_info["status"] = "SUCCESS"
            quality_tests.append(test_info)

        if not val_config.get("allow_duplicates_dates", False) and self.time_column in df.columns:
            dup_dates = int(df.duplicated(subset=[self.time_column]).sum())
            test_info = {"name": "Duplicate dates check", "target": self.time_column, "dup_count": dup_dates}
            if dup_dates > 0:
                test_info["status"] = self.severities.get("quality", "WARNING")
                test_info["error"] = f"Found {dup_dates} records with duplicate dates."
                quality_errors.append(f"Existen {dup_dates} registros con fechas duplicadas.")
            else:
                test_info["status"] = "SUCCESS"
            quality_tests.append(test_info)

        # 3. Centinelas
        if not val_config.get("allow_sentinel_values", False):
            sentinels = thresholds.get("sentinel_values", {})
            num_sentinels = sentinels.get("numeric", [])
            cat_sentinels = sentinels.get("categorical", [])
            
            for col in df.columns:
                found_sentinels = []
                if df[col].dtype in ['int64', 'float64']:
                    found_sentinels = [v for v in num_sentinels if (df[col] == v).any()]
                else:
                    found_sentinels = [v for v in cat_sentinels if (df[col].astype(str).str.strip().str.upper() == str(v).upper()).any()]
                
                test_info = {"name": f"Sentinel check: {col}", "target": col}
                if found_sentinels:
                    test_info["status"] = self.severities.get("quality", "WARNING")
                    test_info["error"] = f"Found sentinel values: {found_sentinels}"
                    quality_errors.append(f"Valores centinela detectados en {col}: {found_sentinels}")
                else:
                    test_info["status"] = "SUCCESS"
                quality_tests.append(test_info)

        status_qual = "SUCCESS" if not quality_errors else self.severities.get("quality", "WARNING")
        results["quality"] = {"status": status_qual, "errors": quality_errors, "tests": quality_tests}
        if status_qual == "FAILED": max_severity = "FAILED"
        elif status_qual == "WARNING" and max_severity == "SUCCESS": max_severity = "WARNING"

        # D. Negocio: Custom Rules [SPEC-PIP-01]
        business_errors = []
        business_tests = []
        custom_rules = rules.get("custom_rules", [])
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        for rule_obj in custom_rules:
            rule_name = rule_obj.get("name", "unnamed")
            expression = rule_obj.get("expression", "")
            
            if not expression:
                continue

            # Caso 1: Reglas expansivas (all_fields)
            if "all_fields" in expression:
                for col in numeric_cols:
                    col_expr = expression.replace("all_fields", col)
                    test_info = {"name": f"{rule_name} ({col})", "expression": col_expr, "target": col}
                    try:
                        fail_mask = ~df.eval(col_expr)
                        fail_count = int(fail_mask.sum())
                        if fail_count > 0:
                            test_info["status"] = self.severities.get("business", "WARNING")
                            test_info["fail_count"] = fail_count
                            business_errors.append(f"Regla '{rule_name}' falló en columna {col} ({fail_count} registros).")
                        else:
                            test_info["status"] = "SUCCESS"
                    except Exception as e:
                        test_info["status"] = "ERROR"
                        test_info["error"] = str(e)
                        business_errors.append(f"Error al evaluar regla '{rule_name}' en {col}: {str(e)}")
                    business_tests.append(test_info)
                continue

            # Caso 2: Regla estándar e Implicación
            test_info = {"name": rule_name, "expression": expression}
            try:
                eval_expr = expression
                if "=>" in expression:
                    parts = expression.split("=>")
                    if len(parts) == 2:
                        ant = parts[0].strip()
                        cons = parts[1].strip()
                        eval_expr = f"~({ant}) | ({cons})"
                
                fail_mask = ~df.eval(eval_expr)
                fail_count = int(fail_mask.sum())
                if fail_count > 0:
                    test_info["status"] = self.severities.get("business", "WARNING")
                    test_info["fail_count"] = fail_count
                    business_errors.append(f"Regla '{rule_name}' falló en {fail_count} registros.")
                else:
                    test_info["status"] = "SUCCESS"
            except Exception as e:
                test_info["status"] = "ERROR"
                test_info["error"] = str(e)
                business_errors.append(f"Error al evaluar regla '{rule_name}': {str(e)}")
            
            business_tests.append(test_info)

        status_biz = "SUCCESS" if not business_errors else self.severities.get("business", "WARNING")
        results["business"] = {"status": status_biz, "errors": business_errors, "tests": business_tests}
        if status_biz == "FAILED": max_severity = "FAILED"
        elif status_biz == "WARNING" and max_severity == "SUCCESS": max_severity = "WARNING"

        return results, max_severity

if __name__ == "__main__":
    # Smoke Test
    validator = ContractValidator()
    print("Validator instanciado correctamente.")
