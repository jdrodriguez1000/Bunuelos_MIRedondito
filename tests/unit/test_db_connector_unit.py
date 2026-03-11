import pytest
from unittest.mock import patch, MagicMock
import os
from src.connector.db_connector import DBConnector

@pytest.fixture(autouse=True)
def reset_singleton():
    """Reinicia el Singleton antes de cada prueba."""
    DBConnector._instance = None
    DBConnector._client = None
    DBConnector._service_client = None

def test_singleton_pattern():
    """[REQ-TEST-01] Verifica que DBConnector sea un Singleton."""
    with patch('src.connector.db_connector.create_client'):
        conn1 = DBConnector()
        conn2 = DBConnector()
        assert conn1 is conn2
        assert id(conn1) == id(conn2)

def test_missing_environment_variables():
    """[REQ-TEST-02] Verifica que se lance ValueError si faltan credenciales."""
    with patch.dict(os.environ, {}, clear=True):
        # Aseguramos que no existan variables cargadas
        with patch('os.getenv', return_value=None):
            with pytest.raises(ValueError, match="Faltan credenciales básicas"):
                DBConnector()

def test_get_client_and_service_client_initialization():
    """[REQ-TEST-03] Verifica la inicialización de ambos clientes."""
    mock_client = MagicMock()
    with patch('src.connector.db_connector.create_client', return_value=mock_client):
        with patch.dict(os.environ, {
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key",
            "SUPABASE_SERVICE_ROLE_KEY": "test-service-key"
        }):
            connector = DBConnector()
            assert connector.get_client() == mock_client
            assert connector.get_service_client() == mock_client

def test_get_service_client_fails_if_not_configured():
    """Verifica error al pedir service client sin llave configurada."""
    mock_client = MagicMock()
    with patch('src.connector.db_connector.create_client', return_value=mock_client):
        # Simulamos que no hay service_role_key
        with patch.dict(os.environ, {
            "SUPABASE_URL": "https://test.supabase.co",
            "SUPABASE_KEY": "test-key"
        }):
            with patch('os.getenv', side_effect=lambda k: "val" if k != "SUPABASE_SERVICE_ROLE_KEY" else None):
                connector = DBConnector()
                with pytest.raises(ValueError, match="SUPABASE_SERVICE_ROLE_KEY no configurado"):
                    connector.get_service_client()
