# IMPL Plan: Creación de Contrato de Datos (Stage 1.3)

## 1. RESUMEN DEL CRONOGRAMA Y EQUIPO (Timeline & Resources)

*   **Duración Estimada**: 1 Sprint de 1 semana (Ejecución Ágil/Fast-Track).
*   **Equipo Requerido**:
    *   **1 Data Engineer (100%)**: Responsable de la conectividad, introspección y persistencia local/cloud.
    *   **1 ML Engineer (50%)**: Diseño de la lógica de profiling estadístico e IQR para outliers.
    *   **1 Technical Delivery Manager (20%)**: Coordinación de ritos, QA y cierre de etapa.

---

## 2. RUTA CRÍTICA Y DEPENDENCIAS (Critical Path)

1.  **Dependencia Bloqueante**: La estructura de la tabla `sys_data_contract` en Supabase debe estar lista antes de iniciar la codificación de la persistencia cloud.
2.  **Ruta Crítica**: `ConfigLoader` -> `Schema Introspector` -> `Stats Engine` -> `Hybrid Persistence`.
3.  **Paralelismo**: El diseño de los tests unitarios puede iniciar en paralelo con la construcción del `Stats Engine` utilizando datos sintéticos (Mocks).

---

## 3. PRODUCT BACKLOG Y WBS (Work Breakdown Structure)

### Épica: Infraestructura y Configuración [EP-01]
*   **Tarea 1.1: Setup de config.yaml [REQ-CFG-01]**
    *   Definición de parámetros para las 9 fuentes maestros [DAT-01] a [DAT-09].
    *   *Responsable*: Data Engineer.
*   **Tarea 1.2: SQL DDL en Supabase [REQ-PER-01]**
    *   Creación de la tabla `sys_data_contract`.
    *   *Responsable*: Backend/Data Engineer.

### Épica: Motor de Introspección y Perfilamiento [EP-02]
*   **Tarea 2.1: Implementación de Introspector Dinámico [REQ-INT-01]**
    *   Lectura de metadatos desde Supabase sin descarga de datos.
    *   *Responsable*: Data Engineer.
*   **Tarea 2.2: Spike: Algoritmo de Outliers e IQR [REQ-STA-01]**
    *   Investigación y validación de la lógica de límites (Timeboxed: 4h).
    *   *Responsable*: ML Engineer.
*   **Tarea 2.3: Desarrollo de StatsEngine [REQ-STA-01]**
    *   Cálculo de medias, percentiles y frecuencias categóricas.
    *   *Responsable*: ML Engineer.

### Épica: Persistencia y Reportabilidad [EP-03]
*   **Tarea 3.1: Manager de Triple Persistencia [REQ-PER-01]**
    *   Escritura en `/contract/contracts/`, `/contract/support/` y Supabase.
    *   *Responsable*: Data Engineer.
*   **Tarea 3.2: Generador de Reporte Builder [REQ-REP-01] [MET-INF-01]**
    *   Captura de métricas de ejecución y latencia.
    *   *Responsable*: Data Engineer.

---

## 4. PLANIFICACIÓN DEL SPRINT (Sprint Roadmap)

### Sprint 1: "The Golden Contract"
*   **Objetivo**: Generar el primer contrato de datos válido y persistirlo en la nube.
*   **Día 1-2**: Configuración, Conectividad e Introspección Dinámica.
*   **Día 3-4**: Desarrollo del motor estadístico y lógica de Outliers.
*   **Día 5**: Integración de persistencia triple, generación de reportes y cierre.

---

## 5. PLAN DE PRUEBAS Y QA (Quality Assurance)

*   **Pruebas Unitarias**: Validar que el `ConfigLoader` rechace archivos YAML mal formados.
*   **Pruebas de Integración**: Verificar que el flag `is_active` en Supabase se actualice atómicamente ([REQ-INV-01]).
*   **Validación de Datos**: Comparar los resultados del `StatsEngine` contra un cálculo manual en Excel/Minitab para una muestra pequeña (Sanity Check).
*   **UAT (User Acceptance)**: Presentación del `builder_report.json` al Product Owner para validar que el tiempo de ejecución es aceptable ([MET-INF-01]).

---

## 6. RITOS ÁGILES Y GOBERNANZA

*   **Daily Standup**: 10 min (Estado, Bloqueos).
*   **Refinamiento**: 30 min (mitad del Sprint) para ajustar reglas customizadas.
*   **Sprint Review / DoD**: Cierre de la fase al cumplir con la "Definición de Hecho" (DoD) de la Etapa 1.3:
    1.  Código en `src/builder.py` sin errores de linter.
    2.  Contrato registrado exitosamente en la nube.
    3.  Reporte ejecutivo de latencia generado.

---
> [!TIP]
> La prioridad máxima es la **Triple Persistencia**. Si el tiempo apremia, se priorizará la estabilidad del contrato YAML sobre la profundidad de las estadísticas categóricas.
