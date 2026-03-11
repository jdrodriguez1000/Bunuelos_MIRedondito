import pytest
import os
import hashlib
from src.builder import DataContractBuilder
from unittest.mock import MagicMock

def test_calculate_md5_consistency(tmp_path):
    """Verifica que el cálculo del MD5 sea correcto y consistente"""
    # Arrange
    content = b"test data for md5"
    test_file = tmp_path / "test.txt"
    test_file.write_bytes(content)
    
    expected_hash = hashlib.md5(content).hexdigest()
    builder = DataContractBuilder()
    
    # Act
    calculated_hash = builder._calculate_md5(str(test_file))
    
    # Assert
    assert calculated_hash == expected_hash

def test_calculate_md5_missing_file():
    """Verifica el comportamiento cuando el archivo no existe"""
    builder = DataContractBuilder()
    assert builder._calculate_md5("non_existent_file.json") == "unknown"

def test_contract_id_generation():
    """Verifica que el builder genere un UUID válido en cada run"""
    builder = DataContractBuilder()
    
    # Mock de métodos pesados para solo probar el inicio de run
    builder.config_loader = MagicMock()
    builder.db = MagicMock()
    builder._persist = MagicMock(return_value="mock_hash")
    builder._save_report = MagicMock()
    
    # Act
    builder.run()
    
    # El primer argumento de _persist (en el llamado real) no lo tenemos fácil aquí,
    # pero podemos verificar que _save_report recibió un execution_id (UUID)
    args, _ = builder._save_report.call_args
    execution_id = args[0]['execution_id']
    
    # Assert
    assert len(execution_id) == 36 # Longitud estándar de UUID
