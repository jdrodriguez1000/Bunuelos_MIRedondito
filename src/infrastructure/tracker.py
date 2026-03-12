from datetime import datetime, timezone
import os
import json
from src.connector.db_connector import DBConnector

class ExecutionTracker:
    """
    Gestor de Auditoría y Semaforización.
    Encargado de persistir el estado de ejecución y los resultados del contrato.
    [REQ-OUT-02], [REQ-OUT-03]
    """

    def __init__(self):
        self.db = DBConnector()
        self.execution_id = None
        self.contract_id = None

    def start_pipeline_execution(self, phase: str, mode: str, contract_id: int, watermark_start: datetime = None, validation_type: str = None) -> str:
        """
        Registra el inicio de una ejecución en sys_pipeline_execution.
        Retorna el ID de la ejecución (UUID).
        """
        self.contract_id = contract_id
        
        try:
            data = {
                "phase": phase,
                "mode": mode,
                "contract_id": contract_id,
                "validation_status": "SUCCESS", # Default inicial
                "execution_status": "IN_PROGRESS",
                "validation_type": validation_type,
                "watermark_start": watermark_start.isoformat() if watermark_start else None,
                "start_at": datetime.now(timezone.utc).isoformat()
            }
            
            response = self.db.get_client().table("sys_pipeline_execution").insert(data).execute()
            
            if response.data:
                self.execution_id = response.data[0]["id"]
                return self.execution_id
            raise Exception("No se pudo obtener el ID de ejecución tras el insert.")
            
        except Exception as e:
            print(f"Error al iniciar auditoría de pipeline: {e}")
            raise

    def log_validation_details(self, table_name: str, status: str, details: dict, latency_ms: int):
        """
        Registra los resultados granulares en sys_validation_contract.
        """
        # Si no hay ID de contrato (ej. fallo de integridad), no podemos insertar en esta tabla
        # por la restricción de llave foránea. El error quedará solo en sys_pipeline_execution.
        if not self.contract_id:
            print(f"⚠️ Saltando log_validation_details: No hay contract_id válido para la tabla {table_name}.")
            return

        try:
            data = {
                "contract_id_ref": self.contract_id,
                "table_name": table_name,
                "status": status,
                "error_details": details,
                "latency_ms": latency_ms,
                "validation_timestamp": datetime.now(timezone.utc).isoformat()
            }
            self.db.get_client().table("sys_validation_contract").insert(data).execute()
        except Exception as e:
            print(f"Error al loguear detalles de validación: {e}")

    def end_pipeline_execution(self, status: str, validation_status: str, watermark_end: datetime = None, error_summary: str = None, metadata: dict = None, watermark_start: datetime = None, validation_type: str = None):
        """
        Cierra el registro de ejecución actualizando el semáforo global.
        """
        if not self.execution_id:
            return

        try:
            data = {
                "execution_status": status,
                "validation_status": validation_status,
                "last_step_completed": "VALIDATE" if status == "COMPLETED" or status == "SKIPPED" else "FAILED_VALIDATION",
                "watermark_end": watermark_end.isoformat() if watermark_end else None,
                "error_summary": error_summary,
                "metadata": metadata,
                "end_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Solo actualizar si vienen en el cierre (útil si se calcularon después del inicio)
            if watermark_start:
                data["watermark_start"] = watermark_start.isoformat()
            if validation_type:
                data["validation_type"] = validation_type
            
            # DEBUG
            # print(f"DEBUG: Enviando PATCH a sys_pipeline_execution con ID {self.execution_id}: {data}")
            
            self.db.get_client().table("sys_pipeline_execution").update(data).eq("id", self.execution_id).execute()
        except Exception as e:
            print(f"Error al cerrar auditoría de pipeline: {e}")

    def generate_local_report(self, path: str, results: dict):
        """
        Genera un archivo JSON local con el resumen de la validación.
        Implementa DOBLE PERSISTENCIA: Fijo + Histórico. [REQ-REP-01]
        """
        try:
            # 1. Guardar archivo FIJO
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            
            # 2. Guardar archivo HISTÓRICO (Doble Persistencia)
            dir_name = os.path.dirname(path)
            file_name = os.path.basename(path)
            name, ext = os.path.splitext(file_name)
            
            history_dir = os.path.join(dir_name, "history")
            os.makedirs(history_dir, exist_ok=True)
            
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            history_path = os.path.join(history_dir, f"{name}_{timestamp}{ext}")
            
            with open(history_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
                
            print(f"✅ Doble persistencia local completada: {path} y {history_path}")
        except Exception as e:
            print(f"Error al generar reporte local (doble persistencia): {e}")

if __name__ == "__main__":
    # Smoke Test dummy
    tracker = ExecutionTracker()
    print("Tracker inicializado corectamente.")
