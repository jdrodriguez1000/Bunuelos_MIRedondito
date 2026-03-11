import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

class DBConnector:
    """
    Conector Universal de Base de Datos para el proyecto Mi Redondito.
    Implementa el patrón Singleton para asegurar una única instancia del cliente.
    Agnóstico al consumidor: expone el cliente de Supabase actual pero centraliza la lógica.
    """
    _instance = None
    _client = None
    _service_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnector, cls).__new__(cls)
            cls._instance._initialize_clients()
        return cls._instance

    def _initialize_clients(self):
        """
        Inicializa los clientes de Supabase utilizando las llaves del archivo .env.
        Requiere: SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY.
        """
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not url or not key:
            raise ValueError("Faltan credenciales básicas de Supabase (URL o KEY) en el archivo .env")

        try:
            # Cliente estándar (anon key)
            self._client = create_client(url, key)
            
            # Cliente con privilegios (service role) si está disponible
            if service_role_key:
                self._service_client = create_client(url, service_role_key)
        except Exception as e:
            print(f"Error al inicializar el cliente de Supabase: {e}")
            raise

    def get_client(self) -> Client:
        """
        Retorna el cliente estándar de Supabase (con RLS activo).
        """
        return self._client

    def get_service_client(self) -> Client:
        """
        Retorna el cliente con rol de servicio (Bypass RLS). 
        Usar con extrema precaución solo en procesos administrativos o de ingesta.
        """
        if not self._service_client:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY no configurado en el entorno.")
        return self._service_client

    def test_connection(self):
        """
        Realiza una prueba de conexión básica.
        """
        try:
            # Intento de lectura mínima para validar el enlace
            # Nota: Asume que existe al menos una tabla o endpoint accesible
            response = self._client.table("ventas").select("count", count="exact").limit(1).execute()
            return True, f"Conexión exitosa. Filas detectadas en 'ventas': {response.count}"
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

if __name__ == "__main__":
    # Smoke Test
    try:
        connector = DBConnector()
        success, message = connector.test_connection()
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    except Exception as e:
        print(f"💥 Error crítico: {e}")
