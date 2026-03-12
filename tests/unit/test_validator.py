import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.validator import ContractValidator

@pytest.fixture
def validator():
    """
    Configura el validador con mocks para evitar efectos secundarios.
    """
    with patch('src.validator.ConfigLoader') as MockConfig, \
         patch('src.validator.ExecutionTracker') as MockTracker, \
         patch('src.validator.DBConnector') as MockDB, \
         patch('src.validator.WatermarkManager') as MockWM:
        
        # Configuramos el mock de ConfigLoader
        mock_config_instance = MockConfig.return_value
        mock_config_instance.config = {
            "validation_mvp": {
                "source": "ventas",
                "time_column": "fecha",
                "rules_severity": "structural:FAILED,continuity:WARNING"
            },
            "thresholds": {"structural": 1.0},
            "storage": {"artifacts": {"data_contract_file": "dummy.yaml"}}
        }
        mock_config_instance.get_contract_rules.return_value = {
            "schema": {"fecha": "datetime64[ns]", "valor": "float64"},
            "validations": {"check_freshness": True}
        }
        
        v = ContractValidator(phase="validation_mvp")
        return v

def test_structural_validation_success(validator):
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2026-01-01"]),
        "valor": [10.5]
    })
    rules = validator.config_loader.get_contract_rules()
    results, severity = validator._run_core_validations(df, rules, "daily")
    
    assert results["structural"]["status"] == "SUCCESS"
    assert len(results["structural"]["errors"]) == 0

def test_structural_validation_missing_column(validator):
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2026-01-01"])
    })
    rules = validator.config_loader.get_contract_rules()
    results, severity = validator._run_core_validations(df, rules, "daily")
    
    assert results["structural"]["status"] == "FAILED"
    assert any("Columna faltante: valor" in err for err in results["structural"]["errors"])

def test_freshness_daily_stale_data(validator):
    today = pd.Timestamp("2026-03-11")
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2026-03-09"]),
        "valor": [1.0]
    })
    rules = validator.config_loader.get_contract_rules()
    
    with patch('pandas.Timestamp.now', return_value=today):
        results, severity = validator._run_core_validations(df, rules, "daily")
        
    stale_test = next(t for t in results["continuity"]["tests"] if t["name"] == "Stale Data check")
    assert stale_test["status"] == "FAILED"

def test_freshness_daily_data_leakage(validator):
    today = pd.Timestamp("2026-03-11")
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2026-03-11"]),
        "valor": [1.0]
    })
    rules = validator.config_loader.get_contract_rules()
    
    with patch('pandas.Timestamp.now', return_value=today):
        results, severity = validator._run_core_validations(df, rules, "daily")
        
    leak_test = next(t for t in results["continuity"]["tests"] if t["name"] == "Data Leakage check")
    assert leak_test["status"] == "FAILED"
