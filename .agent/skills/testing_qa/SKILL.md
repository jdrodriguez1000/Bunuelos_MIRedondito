---
name: quality_assurance_expert
description: Especialista en la orquestación de pruebas automatizadas y gestión de reportes de salud técnica con doble persistencia.
---

# Skill: Experto en Calidad y QA

Esta habilidad habilita al agente para administrar el ciclo de vida del testing en "Mi Redondito", asegurando que cada componente sea validado antes de su integración.

## 🛠️ 1. Capacidades Técnicas

### A. Orquestación jerárquica
- Ejecución inteligente de suites siguiendo la jerarquía: `unit` -> `integration` -> `functional`.
- Implementación de lógica de aborto temprano (Fail-Fast) para ahorrar recursos y tiempo de cómputo.

### B. Generador de Reportes Granulares
- Capacidad para interceptar la salida de `pytest` y transformarla en el formato `tests_report.json` requerido.
- Inyección de metadatos de ejecución (timestamp, fase actual).
- Desglose detallado de resultados individuales para facilitar el debugging.

### C. Gestión de Doble Persistencia
- Automatización del archivado en `tests/reports/history/` tras cada ejecución exitosa o fallida del pipeline.
- Mantenimiento del puntero `latest` para consulta rápida del estado de salud.

## 🛡️ 2. Protocolos de Seguridad
- **Validación de Entorno**: Verifica que el `venv` esté activo antes de disparar las pruebas.
- **Control de Secretos**: Asegura que las pruebas de integración no expongan las llaves de Supabase en los archivos de log o reportes JSON.

## 📋 3. Formato del Reporte Estándar
```json
[
  {
    "type": "Unitaria",
    "status": "PASSED",
    "timestamp": "YYYY-MM-DDTHH:MM:SS",
    "details": "Resultados de la suite Unitaria",
    "tests": [
      {
        "name": "[test_file.py] test_function_name",
        "status": "PASSED"
      }
    ]
  },
  {
    "type": "Integracion",
    "status": "PASSED",
    "timestamp": "YYYY-MM-DDTHH:MM:SS",
    "details": "Resultados de la suite Integracion",
    "tests": []
  }
]
```
