import os
import yaml
import json
import logging
import uuid
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
from src.connector.db_connector import DBConnector

# Configuración de Logging [REQ-REP-01]
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DataContractBuilder")

class ConfigLoader:
    """Carga y valida el archivo config.yaml [REQ-CFG-01]"""
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load()

    def _load(self) -> Dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_sources(self) -> List[Dict]:
        return self.config.get("data_sources", [])

    def get_storage_paths(self) -> Dict:
        return self.config.get("storage", {}).get("local", {})

    def get_profiling_config(self) -> Dict:
        return self.config.get("profiling", {})

class StatsEngine:
    """Calcula el perfilamiento estadístico de los datos [REQ-STA-01]"""
    @staticmethod
    def get_numeric_stats(df: pd.DataFrame, columns: List[str], config: Dict) -> Dict:
        stats = {}
        for col in columns:
            if col not in df.columns: continue
            series = df[col]
            
            # Cálculo de Q1, Q3 e IQR para Outliers [REQ-STA-01]
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            multiplier = config.get("outlier_detection", {}).get("multiplier", 1.5)
            lower_bound = q1 - (multiplier * iqr)
            upper_bound = q3 + (multiplier * iqr)
            
            stats[col] = {
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max()),
                "p25": float(q1),
                "p75": float(q3),
                "outlier_bounds": [float(lower_bound), float(upper_bound)]
            }
        return stats

    @staticmethod
    def get_categorical_stats(df: pd.DataFrame, columns: List[str]) -> Dict:
        stats = {}
        for col in columns:
            if col not in df.columns: continue
            value_counts = df[col].value_counts(normalize=True).to_dict()
            stats[col] = {
                "unique_values": int(df[col].nunique()),
                "distribution": {str(k): float(v) for k, v in value_counts.items()}
            }
        return stats

class DataContractBuilder:
    """Orquestador principal para la creación del contrato de datos"""
    def __init__(self):
        self.config_loader = ConfigLoader()
        self.db = DBConnector()
        self.stats_engine = StatsEngine()
        self.execution_start = datetime.now()

    def _calculate_md5(self, file_path: str) -> str:
        """Calcula el hash MD5 de un archivo para trazabilidad DVC"""
        if not os.path.exists(file_path):
            return "unknown"
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _persist(self, contracts: Dict, statistics: Dict, contract_id: str) -> str:
        paths = self.config_loader.get_storage_paths()
        artifacts = self.config_loader.config.get("storage", {}).get("artifacts", {})
        gen_time = datetime.now().isoformat()
        
        # 1. Local: JSON Statistics (Primero para calcular su hash)
        stats_path = os.path.join(paths["support_dir"], artifacts.get("statistic_file", "statistic_contract.json"))
        os.makedirs(os.path.dirname(stats_path), exist_ok=True)
        stats_final = {
            "contract_id": contract_id,
            "generated_at": gen_time,
            "sources": statistics
        }
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(stats_final, f, indent=4)
        
        # Calculamos el hash del archivo de estadísticas (para trazabilidad interna)
        stats_hash = self._calculate_md5(stats_path)
        
        # 2. Local: YAML Contract (Primero lo escribimos para poder calcular su hash real)
        contract_path = os.path.join(paths["contracts_dir"], artifacts.get("data_contract_file", "data_contract.yaml"))
        os.makedirs(os.path.dirname(contract_path), exist_ok=True)
        contract_final = {
            "version": "1.3",
            "contract_id": contract_id,
            "stats_hash_ref": stats_hash, # Referencia al hash de estadísticas
            "generated_at": gen_time,
            "sources": contracts
        }
        with open(contract_path, "w", encoding="utf-8") as f:
            yaml.dump(contract_final, f, sort_keys=False)

        # 3. El DVC HASH oficial es el hash del archivo de contrato YAML [REQ-HAS-01]
        dvc_hash = self._calculate_md5(contract_path)

        # 4. Cloud: Supabase Persistencia Atómica [REQ-INV-01]
        cloud_config = self.config_loader.config.get("storage", {}).get("cloud", {})
        table_cloud = cloud_config.get("table_name", "sys_data_contract")
        is_active_flag = cloud_config.get("is_active_flag", "is_active")

        try:
            client = self.db.get_service_client()
            # 1. Invalidar contratos anteriores
            client.table(table_cloud).update({is_active_flag: False}).eq(is_active_flag, True).execute()
            
            # 2. Insertar nuevo contrato activo con el mismo ID [REQ-PER-01]
            client.table(table_cloud).insert({
                "contract_id": contract_id,
                "dvc_hash": dvc_hash,
                "data_contract_payload": contracts,
                "statistic_contract_payload": statistics,
                is_active_flag: True
            }).execute()
            logger.info(f"☁️ Contrato {contract_id} (Hash: {dvc_hash}) persistido en Supabase con éxito.")
        except Exception as e:
            logger.error(f"❌ Error en persistencia cloud: {e}")
        
        return dvc_hash

    def run(self):
        logger.info("🚀 Iniciando Data Contract Builder...")
        
        # Generamos el ID único de contrato para trazabilidad total [REQ-PER-01]
        contract_id = str(uuid.uuid4())
        
        sources = self.config_loader.get_sources()
        profiling_config = self.config_loader.get_profiling_config()
        contracts = {}
        statistics = {}

        for source in sources:
            name = source["name"]
            table = source["db_table"]
            logger.info(f"📊 Procesando fuente: {name} (Tabla: {table})")
            
            try:
                # 1. Introspección Dinámica con Paginación [REQ-INT-01]
                # Superamos la restricción de 1000 registros mediante un loop de carga
                client = self.db.get_service_client()
                all_data = []
                chunk_size = 1000
                start = 0
                
                while True:
                    end = start + chunk_size - 1
                    response = client.table(table).select("*").range(start, end).execute()
                    all_data.extend(response.data)
                    
                    if len(response.data) < chunk_size:
                        break
                    start += chunk_size

                df = pd.DataFrame(all_data)

                if df.empty:
                    logger.warning(f"⚠️ La tabla {table} está vacía. Saltando profiling.")
                    continue

                logger.info(f"✅ Total registros cargados para {name}: {len(df)}")

                # 2. Perfilamiento Estadístico
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

                source_stats = {
                    "table_name": table,
                    "row_count": len(df),
                    "numeric_fields": self.stats_engine.get_numeric_stats(df, numeric_cols, profiling_config),
                    "categorical_fields": self.stats_engine.get_categorical_stats(df, cat_cols),
                    "timestamp": datetime.now().isoformat()
                }
                
                statistics[name] = source_stats
                
                # 3. Estructura del Contrato (YAML)
                contracts[name] = {
                    "schema": {col: str(dtype) for col, dtype in df.dtypes.items()},
                    "validations": source.get("validations", {}),
                    "custom_rules": source.get("custom_rules", [])
                }

            except Exception as e:
                logger.error(f"❌ Error procesando {name}: {e}")

        # 4. Persistencia Triple [REQ-PER-01]
        dvc_hash = self._persist(contracts, statistics, contract_id)
        
        execution_end = datetime.now()
        latency = (execution_end - self.execution_start).total_seconds() * 1000
        
        # 5. Reporte de Ejecución [REQ-REP-01]
        report = {
            "execution_id": contract_id,
            "dvc_hash_audit": dvc_hash,
            "timestamp": self.execution_start.isoformat(),
            "latency_ms": latency,
            "sources_processed": list(contracts.keys()),
            "status": "SUCCESS"
        }
        self._save_report(report)
        
        logger.info(f"✅ Ejecución finalizada en {latency:.2f}ms")

    def _save_report(self, report: Dict):
        paths = self.config_loader.get_storage_paths()
        artifacts = self.config_loader.config.get("storage", {}).get("artifacts", {})
        reports_dir = paths["reports_dir"]
        report_file = artifacts.get("report_file", "builder_report.json")
        report_path = os.path.join(reports_dir, report_file)
        
        # 1. Latest Report
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        
        # 2. History Report (Doble Persistencia)
        try:
            history_dir = os.path.join(reports_dir, "history")
            os.makedirs(history_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = report_file.replace(".json", "")
            history_path = os.path.join(history_dir, f"{report_name}_{timestamp}.json")
            
            with open(history_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4)
            
            logger.info(f"✅ Doble persistencia completada: {report_path} y {history_path}")
        except Exception as e:
            logger.warning(f"⚠️ Falló la persistencia histórica: {e}")
            logger.info(f"📄 Reporte de ejecución guardado en: {report_path}")


if __name__ == "__main__":
    builder = DataContractBuilder()
    builder.run()
