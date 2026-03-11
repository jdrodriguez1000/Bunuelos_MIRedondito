import json
import os
from datetime import datetime

def consolidate_reports(raw_json_path, output_path):
    if not os.path.exists(raw_json_path):
        print(f"Error: No se encontró el reporte crudo en {raw_json_path}")
        return

    with open(raw_json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    unit_tests = []
    integration_tests = []
    
    # Extraer pruebas de la data cruda de pytest-json-report
    for test in raw_data.get('tests', []):
        nodeid = test.get('nodeid', '')
        # Formatear nombre como "[archivo.py] nombre_test"
        filename = os.path.basename(nodeid.split('::')[0])
        test_name = nodeid.split('::')[-1]
        formatted_name = f"[{filename}] {test_name}"
        
        status = test.get('outcome', 'UNKNOWN').upper()
        
        test_info = {
            "name": formatted_name,
            "status": status
        }
        
        if 'tests/unit' in nodeid:
            unit_tests.append(test_info)
        elif 'tests/integration' in nodeid:
            integration_tests.append(test_info)

    # Determinar status global de cada suite
    def get_suite_status(tests):
        if not tests: return "PASSED"
        return "FAILED" if any(t['status'] == 'FAILED' for t in tests) else "PASSED"

    timestamp = datetime.now().isoformat()

    # Construir los dos bloques principales
    report_content = [
        {
            "type": "Unitaria",
            "status": get_suite_status(unit_tests),
            "timestamp": timestamp,
            "details": "Resultados de la suite Unitaria",
            "tests": unit_tests
        },
        {
            "type": "Integracion",
            "status": get_suite_status(integration_tests),
            "timestamp": timestamp,
            "details": "Resultados de la suite Integracion",
            "tests": integration_tests
        }
    ]

    # Guardar reporte consolidado
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_content, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Reporte consolidado generado en {output_path}")

if __name__ == "__main__":
    consolidate_reports('tests/reports/tests_report_raw.json', 'tests/reports/tests_report.json')
