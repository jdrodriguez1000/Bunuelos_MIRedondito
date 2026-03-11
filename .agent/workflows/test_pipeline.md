# Workflow: Pipeline de Calidad (test_pipeline)

Este flujo automatiza la validación técnica del proyecto, garantizando la inmutabilidad de los datos y la transparencia de los resultados.

### Pasos de Ejecución

1. **Preparación y Limpieza**
// turbo
Limpia cachés de python y reportes antiguos para asegurar un inicio limpio.
```powershell
if (Test-Path .pytest_cache) { Remove-Item -Recurse -Force .pytest_cache }
```

2. **Ejecución Total y Generación Cruda**
// turbo
Ejecuta todas las pruebas y genera el archivo base de resultados.
```powershell
$env:PYTHONPATH="."; pytest tests/ --json-report --json-report-file=tests/reports/tests_report_raw.json
```

3. **Consolidación de Reporte (Doble Persistencia)**
// turbo
Transforma los resultados crudos en el reporte oficial con formato de bloques (Unitaria/Integración).
```powershell
python scripts/consolidate_reports.py
```

4. **Archivado Histórico**
// turbo
Copia el reporte generado a la carpeta de historial con timestamp.
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"; Copy-Item "tests/reports/tests_report.json" "tests/reports/history/tests_report_$timestamp.json"
```
*Nota: Se implementará un script de consolidación en la fase de construcción de pruebas.*

---
> [!TIP]
> Puedes ejecutar este flujo completo usando el comando `/test_pipeline` en el chat del Agente.
