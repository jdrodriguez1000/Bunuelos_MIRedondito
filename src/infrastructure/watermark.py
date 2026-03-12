from datetime import datetime, timezone
from src.connector.db_connector import DBConnector

class WatermarkManager:
    """
    Controlador de Sincronización Temporal (Watermarking).
    Determina el delta de datos a procesar para evitar validaciones redundantes.
    [REQ-WAT-01]
    """

    def __init__(self):
        self.db = DBConnector()

    def get_last_successful_watermark(self, phase: str, contract_id: int) -> datetime:
        """
        Recupera el último watermark_end exitoso de sys_pipeline_execution.
        """
        try:
            response = self.db.get_client().table("sys_pipeline_execution")\
                .select("watermark_end")\
                .eq("phase", phase)\
                .eq("contract_id", contract_id)\
                .eq("validation_status", "SUCCESS")\
                .eq("execution_status", "COMPLETED")\
                .order("end_at", desc=True)\
                .limit(1)\
                .execute()
            
            if response.data and response.data[0]["watermark_end"]:
                val = response.data[0]["watermark_end"]
                # Normalizar a offset-aware
                dt = datetime.fromisoformat(val)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            return None
        except Exception as e:
            print(f"Error al obtener último watermark: {e}")
            return None

    def get_current_max_date(self, table_name: str, date_column: str) -> datetime:
        """
        Consulta la fecha máxima actual en la tabla de datos.
        """
        try:
            # Query dinámica para obtener el max de la columna de tiempo
            response = self.db.get_client().table(table_name)\
                .select(date_column)\
                .order(date_column, desc=True)\
                .limit(1)\
                .execute()
            
            if response.data and response.data[0][date_column]:
                # Supabase suele retornar strings ISO
                val = response.data[0][date_column]
                dt = None
                if isinstance(val, str):
                    dt = datetime.fromisoformat(val.replace('Z', '+00:00'))
                else:
                    dt = val
                
                # Forzar UTC si es naive
                if dt and dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            return None
        except Exception as e:
            print(f"Error al obtener fecha máxima de {table_name}: {e}")
            return None

    def evaluate_sync_type(self, last_watermark: datetime, current_max: datetime) -> dict:
        """
        Compara los watermarks y determina el tipo de ejecución.
        """
        if current_max is None:
            return {"type": "ERROR", "message": "No se encontraron datos en la tabla fuente."}

        if last_watermark is None:
            return {
                "type": "FULL",
                "start": None,
                "end": current_max,
                "message": "Primera ejecución detectada. Validación completa."
            }

        if current_max > last_watermark:
            return {
                "type": "INCREMENTAL",
                "start": last_watermark,
                "end": current_max,
                "message": f"Nuevos datos detectados desde {last_watermark}."
            }

        if current_max <= last_watermark:
            return {
                "type": "NO_NEW_DATA",
                "start": last_watermark,
                "end": current_max,
                "message": "Los datos ya están validados hasta la fecha actual."
            }
        
        return {"type": "UNKNOWN", "message": "Estado de sincronización inconsistente."}

if __name__ == "__main__":
    # Smoke Test
    wm = WatermarkManager()
    print("WatermarkManager inicializado.")
