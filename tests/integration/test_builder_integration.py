import pytest
from unittest.mock import MagicMock, patch
from src.builder import DataContractBuilder
import pandas as pd

@patch('src.builder.DBConnector')
def test_builder_full_cycle_mocked(mock_db_class):
    """
    Simula una ejecución completa del builder.
    Valida que se llame a la persistencia local y cloud correctamente.
    """
    # Arrange
    mock_db = mock_db_class.return_value
    mock_client = MagicMock()
    mock_db.get_service_client.return_value = mock_client
    
    # Simular respuesta de tabla (paginación de 1 página)
    mock_response = MagicMock()
    mock_response.data = [{'id': 1, 'name': 'test'}]
    mock_client.table.return_value.select.return_value.range.return_value.execute.return_value = mock_response
    
    builder = DataContractBuilder()
    
    # Act
    # Solo procesamos una fuente para velocidad
    with patch.object(builder.config_loader, 'get_sources', return_value=[{
        "name": "test_source",
        "db_table": "dummy_table",
        "validations": {}
    }]):
        builder.run()
    
    # Assert
    # Verificar que se intentó insertar en Supabase
    assert mock_client.table.called
    # El nombre de la tabla por defecto es sys_data_contract
    mock_client.table.assert_any_call('sys_data_contract')
    # Verificar que se llamó a insert
    assert mock_client.table().insert.called
