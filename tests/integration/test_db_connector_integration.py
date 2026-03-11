import pytest
from src.connector.db_connector import DBConnector

def test_db_connection_real():
    """[REQ-TEST-04] Prueba de Humo: Verifica conectividad real con Supabase."""
    try:
        # Reiniciamos el singleton para asegurar carga fresca de .env
        DBConnector._instance = None
        connector = DBConnector()
        success, message = connector.test_connection()
        
        assert success is True, f"La conexión falló: {message}"
        assert "viva" in message.lower() or "detectadas" in message.lower()
        
    except Exception as e:
        pytest.fail(f"Error crítico durante la prueba de integración: {e}")

def test_singleton_consistency_in_integration():
    """Verifica que el Singleton se mantiene consistente entre llamadas de integración."""
    conn1 = DBConnector()
    conn2 = DBConnector()
    assert id(conn1) == id(conn2)
