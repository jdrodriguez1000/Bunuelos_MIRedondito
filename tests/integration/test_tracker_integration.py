import pytest
import os
from datetime import datetime, timezone
from src.infrastructure.tracker import ExecutionTracker
from src.connector.db_connector import DBConnector

@pytest.mark.integration
def test_tracker_lifecycle_integration():
    """
    Valida el ciclo de vida completo de la auditoría en Supabase.
    Verifica que watermark_start y validation_type se persistan correctamente.
    """
    # Arrange
    tracker = ExecutionTracker()
    phase = "test_integration"
    contract_id = 13 # Inventario detallado sandbox
    watermark_start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    validation_type = "FULL"
    
    # Act - Inicio
    execution_id = tracker.start_pipeline_execution(
        phase=phase,
        mode="test",
        contract_id=contract_id,
        watermark_start=watermark_start,
        validation_type=validation_type
    )
    
    assert execution_id is not None
    assert tracker.execution_id == execution_id
    
    # Act - Cierre
    tracker.end_pipeline_execution(
        status="SKIPPED",
        validation_status="SUCCESS",
        watermark_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        error_summary="Prueba de integración exitosa",
        watermark_start=watermark_start,
        validation_type=validation_type
    )
    
    # Assert - Verificación en DB
    db = DBConnector()
    client = db.get_client()
    response = client.table("sys_pipeline_execution").select("*").eq("id", execution_id).execute()
    
    assert len(response.data) == 1
    record = response.data[0]
    
    assert record["phase"] == phase
    assert record["validation_type"] == validation_type
    assert "2026-01-01" in record["watermark_start"]
