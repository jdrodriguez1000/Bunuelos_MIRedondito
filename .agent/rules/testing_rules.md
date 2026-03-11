# REGLAS DE TESTING Y CALIDAD (TESTING_RULES)

## 1. Identificación y Control (Metadata)
*   **Título:** Reglas de Testing y Aseguramiento de Calidad
*   **Versión:** v1.1.0
*   **Estado:** Oficial / Aprobado
*   **Trazabilidad:** Alineado con el Project Charter de Mi Redondito.

---

## 🛡️ 2. Inmutabilidad y Aislamiento
- **Aislamiento Total (Unit)**: Las pruebas en `tests/unit/` deben ser 100% offline. Uso obligatorio de **Mocks** para el conector de base de datos.
- **Protección de Producción**: Queda prohibida la alteración de datos reales. Las pruebas de integración deben usar credenciales de Sandbox o realizar operaciones de solo lectura.

## 🏗️ 3. Estructura y Jerarquía
- **Directorio Raíz**: `tests/`
- **Subcarpetas Obligatorias**:
    - `unit/`: Lógica pura, transformaciones y cálculos (MAPE/Métricas).
    - `integration/`: Validación de conectores (Supabase) y carga de secrets (.env).
    - `functional/`: Flujos E2E de forecasting y generación de proyecciones.
    - `reports/`: Almacenamiento de resultados y auditoría.
- **Fail-Fast**: Si falla una prueba unitaria, la suite de integración y funcional NO se ejecuta.

## 🧪 4. Estándares de Implementación
- **Framework**: Uso mandatorio de `pytest`.
- **Naming**: Archivos: `test_*.py`. Funciones: `test_[nombre_descriptivo_de_la_accion]`.
- **Patrón AAA**: Todas las pruebas deben estructurarse en **Arrange** (Preparar), **Act** (Ejecutar) y **Assert** (Validar).

## 📊 5. Protocolo de Reportes (Doble Persistencia)
- **Nombre de Archivo**: `tests_report.json`
- **Ubicación Latest**: `tests/reports/tests_report.json`
- **Ubicación Histórico**: `tests/reports/history/tests_report_YYYYMMDD_HHMMSS.json`
- **Contenido Requerido**:
    - Metadatos: Fecha de ejecución, Fase del proyecto, Usuario/Agente.
    - Detalle: Resultados **prueba por prueba** (Nombre, Clase, Estado: PASSED/FAILED, Mensaje de error si aplica).
