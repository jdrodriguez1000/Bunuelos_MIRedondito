import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def run_sql_script():
    """
    Lee el archivo SQL de configuración y lo ejecuta en la base de datos.
    Esto asegura que la tabla y las políticas RLS se creen correctamente.
    """
    sql_path = os.path.abspath("scripts/sql/tables/create_sys_data_contract.sql")
    
    if not os.path.exists(sql_path):
        print(f"❌ Error: No se encontró el archivo SQL en {sql_path}")
        return

    try:
        # Extraer credenciales
        conn_string = f"dbname='{os.getenv('DB_NAME')}' user='{os.getenv('DB_USER')}' host='{os.getenv('DB_HOST')}' password='{os.getenv('DB_PASSWORD')}' port='{os.getenv('DB_PORT')}'"
        
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        
        print(f"📖 Leyendo script: {sql_path}...")
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_commands = f.read()
        
        print("🚀 Ejecutando comandos SQL...")
        cur.execute(sql_commands)
        conn.commit()
        
        print("✅ Infraestructura 'sys_data_contract' (Tabla + RLS) desplegada con éxito.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error durante la ejecución del script: {e}")

if __name__ == "__main__":
    run_sql_script()

