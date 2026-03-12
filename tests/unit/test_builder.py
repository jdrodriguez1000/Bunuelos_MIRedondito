import pytest
import os
import json
import yaml
from unittest.mock import MagicMock, patch
from src.builder import DataContractBuilder

@pytest.fixture
def mock_builder():
    with patch('src.builder.ConfigLoader') as MockConfig, \
         patch('src.builder.DBConnector') as MockDB:
        
        mock_config = MockConfig.return_value
        mock_config.get_storage_paths.return_value = {
            "contracts_dir": "tests/tmp/contracts",
            "support_dir": "tests/tmp/support",
            "reports_dir": "tests/tmp/reports"
        }
        mock_config.config = {
            "storage": {
                "artifacts": {
                    "data_contract_file": "test_contract.yaml",
                    "statistic_file": "test_stats.json",
                    "report_file": "test_report.json"
                },
                "cloud": {
                    "table_name": "test_table",
                    "is_active_flag": "is_active"
                }
            }
        }
        
        builder = DataContractBuilder()
        # Mock de DB client para evitar llamadas reales
        builder.db.get_service_client.return_value = MagicMock()
        return builder

def test_persist_writes_files_correctly(mock_builder, tmp_path):
    # Setup paths to use tmp_path
    mock_builder.config_loader.get_storage_paths.return_value = {
        "contracts_dir": str(tmp_path / "contracts"),
        "support_dir": str(tmp_path / "support"),
        "reports_dir": str(tmp_path / "reports")
    }
    
    contracts = {"source1": {"schema": {"col1": "int"}}}
    statistics = {"source1": {"row_count": 100}}
    contract_id = "test-uuid"
    
    # Act
    dvc_hash = mock_builder._persist(contracts, statistics, contract_id)
    
    # Assert
    contract_file = tmp_path / "contracts" / "test_contract.yaml"
    stats_file = tmp_path / "support" / "test_stats.json"
    
    assert contract_file.exists()
    assert stats_file.exists()
    assert dvc_hash is not None
    
    with open(contract_file, "r") as f:
        data = yaml.safe_load(f)
        assert data["contract_id"] == contract_id
        assert "source1" in data["sources"]

def test_save_report_format(mock_builder, tmp_path):
    mock_builder.config_loader.get_storage_paths.return_value = {
        "reports_dir": str(tmp_path / "reports")
    }
    report = {"status": "SUCCESS", "execution_id": "123"}
    
    mock_builder._save_report(report)
    
    report_file = tmp_path / "reports" / "test_report.json"
    assert report_file.exists()
    with open(report_file, "r") as f:
        data = json.load(f)
        assert data["status"] == "SUCCESS"
