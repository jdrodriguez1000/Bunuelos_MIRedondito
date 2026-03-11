import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from typing import Optional

# Cargar variables de entorno
load_dotenv()

class SupabaseClient:
    """
    Singleton class to manage the connection to Supabase PostgreSQL database.
    Using SQLAlchemy for connection pooling and efficient querying.
    """
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance._initialize_engine()
        return cls._instance

    def _initialize_engine(self):
        """
        Initializes the SQLAlchemy engine using environment variables.
        """
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD") or os.getenv("SUPABASE_DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "db.pkiyyyhslejhacdcotua.supabase.co")
        db_port = os.getenv("DB_PORT", "6543")  # Default to Supabase Pooler
        db_name = os.getenv("DB_NAME", "postgres")

        if not db_password:
            raise ValueError("Database password (DB_PASSWORD) not found in environment variables.")

        # Construct connection string
        # Usingpostgresql+psycopg2://[user]:[password]@[host]:[port]/[database]
        connection_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        try:
            self._engine = create_engine(
                connection_url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )
        except Exception as e:
            print(f"Error creating SQLAlchemy engine: {e}")
            raise

    def get_engine(self):
        """
        Returns the SQLAlchemy engine instance.
        """
        return self._engine

    def test_connection(self):
        """
        Tests the connection to the database by executing a simple SELECT 1.
        Returns the database version and latency if successful.
        """
        import time
        start_time = time.perf_counter()
        
        try:
            with self._engine.connect() as conn:
                result = conn.execute(text("SELECT version();"))
                version = result.fetchone()[0]
                end_time = time.perf_counter()
                latency = (end_time - start_time) * 1000
                return True, version, latency
        except Exception as e:
            return False, str(e), 0

if __name__ == "__main__":
    # Smoke test
    client = SupabaseClient()
    success, detail, latency = client.test_connection()
    if success:
        print(f"Connection Successful!")
        print(f"Version: {detail}")
        print(f"Latency: {latency:.2f} ms")
    else:
        print(f"Connection Failed: {detail}")
