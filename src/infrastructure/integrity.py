import hashlib
import os
from src.connector.db_connector import DBConnector

class IntegrityChecker:
    """
    Componente encargado de garantizar que el contrato de datos local
    coincida exactamente con la versión aprobada en el Cloud (Supabase).
    [REQ-HAS-01]
    """

    def __init__(self, contract_path: str):
        self.contract_path = contract_path
        self.db = DBConnector()

    def _calculate_local_hash(self) -> str:
        """
        Calcula el hash MD5 del archivo de contrato local.
        """
        if not os.path.exists(self.contract_path):
            raise FileNotFoundError(f"No se encontró el contrato en {self.contract_path}")
        
        with open(self.contract_path, "rb") as f:
            file_hash = hashlib.md5()
            chunk = f.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(8192)
        
        return file_hash.hexdigest()

    def verify_integrity(self, table_name: str) -> dict:
        """
        Compara el hash local contra el hash registrado en Supabase.
        Retorna: { 'success': bool, 'local_hash': str, 'cloud_hash': str, 'contract_id': int }
        """
        local_hash = self._calculate_local_hash()
        
        # Consultar el hash en Supabase (sys_data_contract)
        try:
            # Traemos el contrato activo más reciente
            response = self.db.get_client().table("sys_data_contract")\
                .select("id, dvc_hash")\
                .eq("is_active", True)\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()
            
            if not response.data:
                return {
                    "success": False,
                    "error": "No se encontró un contrato activo en Cloud.",
                    "local_hash": local_hash,
                    "cloud_hash": None
                }
            
            cloud_record = response.data[0]
            cloud_hash = cloud_record.get("dvc_hash")
            contract_id = cloud_record.get("id")

            if local_hash == cloud_hash:
                return {
                    "success": True,
                    "local_hash": local_hash,
                    "cloud_hash": cloud_hash,
                    "contract_id": contract_id
                }
            else:
                return {
                    "success": False,
                    "error": "SECURITY_BREACH: El hash local no coincide con la versión aprobada en Cloud.",
                    "local_hash": local_hash,
                    "cloud_hash": cloud_hash,
                    "contract_id": contract_id
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error de conexión al verificar integridad: {str(e)}",
                "local_hash": local_hash,
                "cloud_hash": None
            }

if __name__ == "__main__":
    # Smoke Test
    # Asumiendo que existe un contrato en c:\Users\USUARIO\Documents\Forecaster\Bunuelos_MIRedondito\contract\inventario_detallado.yaml
    path = "contract/inventario_detallado.yaml"
    checker = IntegrityChecker(path)
    result = checker.verify_integrity("inventario_detallado")
    print(result)
