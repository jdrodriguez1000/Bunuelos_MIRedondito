import os
import yaml
import json
import logging
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from src.connector.db_connector import DBConnector
from src.infrastructure.integrity import IntegrityChecker
from src.infrastructure.tracker import ExecutionTracker
from src.infrastructure.watermark import WatermarkManager
from src.builder import ConfigLoader

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ContractValidator")

class ContractValidator:
    """
    Motor Principal de Validación de Contratos de Datos (Gatekeeper).
    Orquesta la seguridad, sincronización y calidad de los datos para múltiples fuentes.
    [ARC-12]
    """

    def __init__(self, phase: str = None):
        """
        Inicializa el validador cargando la configuración de la fase activa.
        """
        self.config_loader = ConfigLoader()
        
        # 1. Determinar Fase Activa [REQ-01]
        if phase is None:
            self.phase_name = self.config_loader.config.get("project", {}).get("active_phase", "MVP")
        else:
            self.phase_name = phase
            
        # 2. Cargar Configuración de Ejecución (Sección 7)
        execution_key = f"validation_{self.phase_name.lower()}"
        self.execution_config = self.config_loader.config.get(execution_key, {})
        
        if not self.execution_config:
            # Fallback a la clave literal si no sigue el patrón validation_xxx
            self.execution_config = self.config_loader.config.get(self.phase_name, {})
            
        if not self.execution_config:
            raise ValueError(f"No se encontró configuración de ejecución para la fase: {self.phase_name}")

        self.db = DBConnector()
        self.tracker = ExecutionTracker()
        self.watermark_mgr = WatermarkManager()
        
        # 3. Setup de Rutas de Contrato
        storage = self.config_loader.config.get("storage", {})
        contracts_dir = storage.get("local", {}).get("contracts_dir", "contract/contracts")
        contract_file = storage.get("artifacts", {}).get("data_contract_file", "data_contract.yaml")
        self.contract_path = os.path.join(contracts_dir, contract_file)
        
        self.integrity_checker = IntegrityChecker(self.contract_path)
        
        # Mapeo de fuentes para acceso rápido
        self.sources_repo = {s["db_table"]: s for s in self.config_loader.get_sources()}
        
        logger.info(f"🚀 Validador inicializado para Fase: {self.phase_name}")

    def is_table_active(self, table_name: str) -> bool:
        """
        Verifica si una tabla está habilitada en el repositorio maestro (Sección 4).
        [ARC-12.2] [REQ-SELECT-01]
        """
        source = self.sources_repo.get(table_name)
        if not source:
            logger.warning(f"⚠️ Tabla {table_name} no encontrada en el repositorio configurado.")
            return False
        
        active = source.get("enabled", False)
        if not active:
            logger.info(f"💤 Tabla {table_name} está desactivada (enabled: false). Ignorando.")
        
        return active

    def validate_pipeline(self, mode: str = "LOAD") -> bool:
        """
        Orquestador principal que itera sobre todas las fuentes definidas para la fase.
        """
        target_sources = self.execution_config.get("target_sources", [])
        if not target_sources:
            logger.warning(f"⚠️ No hay fuentes configuradas en target_sources para la fase {self.phase_name}")
            return True

        overall_success = True
        
        for source_entry in target_sources:
            table_name = source_entry.get("table")
            
            # A. Check Selection Filter [REQ-SELECT-01]
            if not self.is_table_active(table_name):
                continue
                
            logger.info(f"🔍 Procesando validación para: {table_name}")
            
            # B. Fetch Data (Paginado para evitar límites)
            try:
                df = self._fetch_table_data(table_name)
                if df.empty:
                    logger.warning(f"⚠️ Tabla {table_name} está vacía. Saltando validación.")
                    continue
                
                # C. Run Gatekeeper Validation [ARC-12]
                success = self.validate_gate(df, source_entry, mode)
                if not success:
                    overall_success = False
                    
            except Exception as e:
                logger.error(f"❌ Error crítico procesando tabla {table_name}: {str(e)}")
                overall_success = False

        return overall_success

    def _fetch_table_data(self, table_name: str) -> pd.DataFrame:
        """Helper para cargar datos desde Supabase con paginación."""
        client = self.db.get_service_client()
        all_data = []
        chunk_size = 1000
        start = 0
        
        while True:
            end = start + chunk_size - 1
            response = client.table(table_name).select("*").range(start, end).execute()
            all_data.extend(response.data)
            
            if len(response.data) < chunk_size:
                break
            start += chunk_size
            
        return pd.DataFrame(all_data)

    def validate_gate(self, df: pd.DataFrame, source_entry: dict, mode: str = "LOAD") -> bool:
        """
        Ejecuta el flujo completo de validación para UNA fuente específica.
        [ARC-12]
        """
        table_name = source_entry.get("table")
        time_column = source_entry.get("time_column")
        custom_severities = source_entry.get("severities", {})
        
        start_time = datetime.now()
        local_report_path = self.execution_config.get("operational_paths", {}).get("local_report", "outputs/reports/phase_MVP/validation_report.json")
        
        # 1. INTEGRITY CHECK [REQ-HAS-01]
        integrity = self.integrity_checker.verify_integrity(table_name)
        contract_id = integrity.get("contract_id")
        
        # 4. AUDIT INIT
        # Usamos tracker para iniciar el registro en Supabase
        self.tracker.start_pipeline_execution(
            phase=self.phase_name,
            mode=mode,
            contract_id=contract_id if contract_id else None
        )

        if not integrity["success"]:
            error_msg = f"SECURITY_BREACH: {integrity.get('error')}"
            logger.error(f"❌ FALLO DE INTEGRIDAD: {error_msg}")
            
            latency = int((datetime.now() - start_time).total_seconds() * 1000)
            details = {"security": {"status": "FAILED", "errors": [error_msg]}}
            
            # Reporte Local even on Integrity Failure
            try:
                self.tracker.generate_local_report(local_report_path, {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "phase": self.phase_name,
                    "table": table_name,
                    "status": "FAILED",
                    "results": details,
                    "latency_ms": latency,
                    "rows_processed": 0
                })
            except: pass

            self.tracker.log_validation_details(
                table_name=table_name,
                status="FAILED",
                details=details,
                latency_ms=latency
            )
            self.tracker.end_pipeline_execution(
                status="ABORTED",
                validation_status="FAILED",
                error_summary=error_msg
            )
            return False
        
        # 2. WATERMARK CHECK [REQ-WAT-01]
        last_watermark = self.watermark_mgr.get_last_successful_watermark(self.phase_name, contract_id)
        current_max = self.watermark_mgr.get_current_max_date(table_name, time_column if time_column else "updated_at")
        
        sync_eval = self.watermark_mgr.evaluate_sync_type(last_watermark, current_max)
        logger.info(f"🔄 Sync Eval: {sync_eval['type']} para {table_name}")
        
        if sync_eval["type"] == "NO_NEW_DATA":
            logger.info(f"⏭️ No hay datos nuevos para {table_name}. Saltando.")
            
            latency = int((datetime.now() - start_time).total_seconds() * 1000)
            try:
                self.tracker.generate_local_report(local_report_path, {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "phase": self.phase_name,
                    "table": table_name,
                    "status": "SUCCESS",
                    "validation_type": "NO_NEW_DATA",
                    "results": {"sync": {"status": "SUCCESS", "message": "No new data detected since last watermark."}},
                    "rows_processed": 0
                })
            except: pass

            self.tracker.end_pipeline_execution(
                status="SKIPPED", 
                validation_status="SUCCESS", 
                watermark_end=current_max, 
                error_summary="No new data detected.",
                watermark_start=last_watermark,
                validation_type=sync_eval["type"]
            )
            return True 

        # 3. LOAD CONTRACT RULES
        try:
            with open(self.contract_path, "r", encoding="utf-8") as f:
                full_contract = yaml.safe_load(f)
                sources = full_contract.get("sources", {})
                # El contrato usa el alias definido en data_sources.name
                source_alias = next(
                    (s["name"] for s in self.config_loader.get_sources() if s["db_table"] == table_name),
                    table_name
                )
                table_rules = sources.get(source_alias)
                
                if not table_rules:
                    raise ValueError(f"Reglas no encontradas para la fuente '{source_alias}'")
        except Exception as e:
            error_msg = f"Error al cargar reglas de contrato: {str(e)}"
            self.tracker.end_pipeline_execution(status="ABORTED", validation_status="FAILED", error_summary=error_msg)
            return False

        # 5. DATA VALIDATION (Core Logic)
        source_master = self.sources_repo.get(table_name, {})
        frequency = source_master.get("frequency", "daily")
        
        results, global_status = self._run_core_validations(df, table_rules, frequency, custom_severities, time_column)
        
        # 6. PERSISTENCE & CLOSE [REQ-OUT-02]
        latency = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Reporte Local Final (SIEMPRE se debe generar para dar visibilidad al usuario)
        try:
            self.tracker.generate_local_report(local_report_path, {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "phase": self.phase_name,
                "table": table_name,
                "status": global_status,
                "results": results,
                "latency_ms": latency,
                "rows_processed": len(df)
            })
        except Exception as e:
            logger.error(f"⚠️ Error fatal al generar reporte local: {str(e)}")

        # Notificar a la nube (Opcional si falla, no debe romper el flujo local)
        try:
            self.tracker.log_validation_details(
                table_name=table_name,
                status=global_status,
                details=results,
                latency_ms=latency
            )
            
            self.tracker.end_pipeline_execution(
                status="COMPLETED" if global_status != "FAILED" else "ABORTED",
                validation_status=global_status,
                watermark_end=current_max,
                error_summary=None if global_status == "SUCCESS" else "Validación terminada con hallazgos",
                metadata={"rows_processed": len(df), "latency_ms": latency},
                watermark_start=last_watermark,
                validation_type=sync_eval["type"]
            )
        except Exception as e:
            logger.warning(f"⚠️ Error al persistir auditoría en la nube: {str(e)}")

        return global_status != "FAILED"

    def _run_core_validations(self, df: pd.DataFrame, rules: dict, frequency: str, severities: dict, time_col: str) -> (dict, str):
        """
        Ejecuta las pruebas core y genera un reporte detallado con micro-tests.
        """
        results = {}
        max_severity = "SUCCESS"
        val_config = rules.get("validations", {})

        # A. Estructural
        structural_errors = []
        structural_tests = []
        expected_schema = rules.get("schema", {})
        
        for col, expected_dtype in expected_schema.items():
            test_entry = {
                "name": f"Schema check: {col}",
                "target": col,
                "expected": expected_dtype,
                "status": "SUCCESS"
            }
            if col not in df.columns:
                err = f"Falta columna: {col}"
                structural_errors.append(err)
                test_entry["status"] = "FAILED"
                test_entry["error"] = err
            else:
                actual_dtype = str(df[col].dtype)
                test_entry["actual"] = actual_dtype
                match = any(str(exp).lower() in actual_dtype.lower() for exp in expected_dtype)
                if not match:
                    err = f"Type mismatch en {col}: {expected_dtype} vs {actual_dtype}"
                    structural_errors.append(err)
                    test_entry["status"] = "FAILED"
                    test_entry["error"] = err
            structural_tests.append(test_entry)

        status_str = "SUCCESS" if not structural_errors else severities.get("structural", "FAILED")
        results["structural"] = {"status": status_str, "errors": structural_errors, "tests": structural_tests}
        if status_str == "FAILED": max_severity = "FAILED"

        # B. Continuidad y Frescura
        continuity_errors = []
        continuity_tests = []
        if time_col and time_col in df.columns:
            df_dates = pd.to_datetime(df[time_col], errors='coerce').dropna()
            max_date_str = str(df_dates.max()) if not df_dates.empty else "N/A"
            
            # Test: Leakage e Stale (Daily X-1)
            t_leak = {"name": "Data Leakage check", "target": time_col, "status": "SUCCESS", "max_date": max_date_str}
            t_stale = {"name": "Stale Data check", "target": time_col, "status": "SUCCESS", "max_date": max_date_str}
            
            if not df_dates.empty:
                max_date = df_dates.max()
                today = pd.Timestamp.now()
                if frequency == "daily":
                    limit = (today - pd.Timedelta(days=1)).normalize()
                    max_d_naive = max_date.replace(tzinfo=None).normalize()
                    if max_d_naive > limit:
                        err = f"Leakage: {max_d_naive} > {limit}"
                        continuity_errors.append(err)
                        t_leak["status"] = "FAILED"; t_leak["error"] = err
                    if max_d_naive < limit:
                        err = f"Stale: {max_d_naive} < {limit}"
                        continuity_errors.append(err)
                        t_stale["status"] = "FAILED"; t_stale["error"] = err
            
            continuity_tests.extend([t_leak, t_stale])

        status_cont = "SUCCESS" if not continuity_errors else severities.get("continuity", "FAILED")
        results["continuity"] = {"status": status_cont, "errors": continuity_errors, "tests": continuity_tests}
        if status_cont == "FAILED": max_severity = "FAILED"
        elif status_cont == "WARNING" and max_severity == "SUCCESS": max_severity = "WARNING"

        # C. Calidad: Nulos y Duplicados
        quality_errors = []
        quality_tests = []
        
        # Null checks per column
        for col in df.columns:
            null_count = int(df[col].isnull().sum())
            t_null = {"name": f"Null check: {col}", "target": col, "null_count": null_count, "status": "SUCCESS"}
            if not val_config.get("allow_nulls", False) and null_count > 0:
                err = f"Nulos detectados en {col}: {null_count}"
                quality_errors.append(err)
                t_null["status"] = "FAILED"
            quality_tests.append(t_null)
        
        # Duplicate rows
        dup_count = int(df.duplicated().sum())
        t_dup = {"name": "Duplicate rows check", "target": "dataframe", "dup_count": dup_count, "status": "SUCCESS"}
        if not val_config.get("allow_duplicates_rows", False) and dup_count > 0:
            err = f"Existen {dup_count} filas duplicadas"
            quality_errors.append(err)
            t_dup["status"] = "FAILED"
        quality_tests.append(t_dup)

        status_qual = "SUCCESS" if not quality_errors else severities.get("quality", "WARNING")
        results["quality"] = {"status": status_qual, "errors": quality_errors, "tests": quality_tests}
        if status_qual == "FAILED": max_severity = "FAILED"
        elif status_qual == "WARNING" and max_severity == "SUCCESS": max_severity = "WARNING"

        # D. Negocio (Reglas Custom)
        business_errors = []
        business_tests = []
        custom_rules = rules.get("custom_rules", [])
        for rule in custom_rules:
            expr = rule.get("expression")
            t_biz = {"name": rule.get("name"), "expression": expr, "status": "SUCCESS"}
            if expr and "all_fields" not in expr:
                try:
                    eval_expr = expr
                    if "=>" in expr:
                        ant, cons = expr.split("=>")
                        eval_expr = f"~({ant.strip()}) | ({cons.strip()})"
                    fails = int((~df.eval(eval_expr)).sum())
                    if fails > 0:
                        err = f"Regla {rule['name']} falló en {fails} filas"
                        business_errors.append(err)
                        t_biz["status"] = "FAILED"
                        t_biz["fails"] = fails
                except Exception as e:
                    err = f"Error eval {rule['name']}: {str(e)}"
                    business_errors.append(err)
                    t_biz["status"] = "ERROR"; t_biz["error"] = err
            business_tests.append(t_biz)

        status_biz = "SUCCESS" if not business_errors else severities.get("business", "WARNING")
        results["business"] = {"status": status_biz, "errors": business_errors, "tests": business_tests}
        if status_biz == "FAILED": max_severity = "FAILED"
        elif status_biz == "WARNING" and max_severity == "SUCCESS": max_severity = "WARNING"

        return results, max_severity

if __name__ == "__main__":
    validator = ContractValidator()
    # Para probar: validator.validate_pipeline()
