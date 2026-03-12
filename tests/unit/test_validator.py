import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.validator import ContractValidator

@pytest.fixture
def validator():
    """
    Configura el validador con mocks adaptados a la nueva estructura del config.yaml.
    """
    with patch('src.validator.ConfigLoader') as MockConfig, \
         patch('src.validator.ExecutionTracker') as MockTracker, \
         patch('src.validator.DBConnector') as MockDB, \
         patch('src.validator.WatermarkManager') as MockWM, \
         patch('src.validator.IntegrityChecker') as MockIC:
        
        # Configuramos el mock de ConfigLoader
        mock_config_instance = MockConfig.return_value
        mock_config_instance.config = {
            "validation_mvp": {
                "target_sources": [
                    {
                        "table": "inventario_detallado",
                        "time_column": "fecha",
                        "severities": {
                            "structural": "FAILED",
                            "continuity": "FAILED",
                            "quality": "WARNING",
                            "business": "WARNING"
                        }
                    }
                ],
                "operational_paths": {
                    "local_report": "outputs/reports/phase_MVP/validation_report.json"
                }
            },
            "thresholds": {"structural": 1.0},
            "storage": {
                "local": {"contracts_dir": "contract/contracts"},
                "artifacts": {"data_contract_file": "data_contract.yaml"}
            },
            "data_sources": [
                {"name": "inventory", "db_table": "inventario_detallado", "enabled": True}
            ]
        }
        mock_config_instance.get_sources.return_value = [
            {"name": "inventory", "db_table": "inventario_detallado", "enabled": True}
        ]
        
        v = ContractValidator(phase="validation_mvp")
        return v

def test_is_table_active(validator):
    assert validator.is_table_active("inventario_detallado") is True
    assert validator.is_table_active("unknown_table") is False

def test_structural_validation_success(validator):
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2020-01-01"]), # Fecha lejana para evitar lio de continuidad si se activara
        "valor": [10.5]
    })
    rules = {
        "schema": {"fecha": ["datetime64", "object"], "valor": ["float64", "int64"]}
    }
    # Solo nos importa structural para esta prueba, desactivamos el efecto de continuidad
    severities = {"structural": "FAILED", "continuity": "SUCCESS"}
    
    results, status = validator._run_core_validations(df, rules, "daily", severities, "fecha")
    
    assert results["structural"]["status"] == "SUCCESS"
    assert status == "SUCCESS"

def test_structural_validation_missing_column(validator):
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2026-01-01"])
    })
    rules = {
        "schema": {"fecha": ["datetime64", "object"], "valor": ["float64", "int64"]}
    }
    # Desactivamos continuidad para aislar la falla estructural
    severities = {"structural": "FAILED", "continuity": "SUCCESS"}
    
    results, status = validator._run_core_validations(df, rules, "daily", severities, "fecha")
    
    assert results["structural"]["status"] == "FAILED"
    assert any("Falta columna: valor" in err for err in results["structural"]["errors"])
    assert status == "FAILED"

def test_freshness_daily_stale_data(validator):
    today = pd.Timestamp("2026-03-11")
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2026-03-09"]),
        "valor": [1.0]
    })
    rules = {"schema": {"fecha": ["datetime64", "object"]}}
    severities = {"continuity": "FAILED"}
    
    with patch('pandas.Timestamp.now', return_value=today):
        results, status = validator._run_core_validations(df, rules, "daily", severities, "fecha")
        
    assert results["continuity"]["status"] == "FAILED"
    assert any("Stale" in err for err in results["continuity"]["errors"])

def test_freshness_daily_data_leakage(validator):
    today = pd.Timestamp("2026-03-11")
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2026-03-11"]),
        "valor": [1.0]
    })
    rules = {"schema": {"fecha": ["datetime64", "object"]}}
    severities = {"continuity": "FAILED"}
    
    with patch('pandas.Timestamp.now', return_value=today):
        results, status = validator._run_core_validations(df, rules, "daily", severities, "fecha")
        
    assert results["continuity"]["status"] == "FAILED"
    assert any("Leakage" in err for err in results["continuity"]["errors"])
