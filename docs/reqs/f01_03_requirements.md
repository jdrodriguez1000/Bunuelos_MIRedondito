# PRD: Creación de Contrato de Datos (Stage 1.3)

## 1. RESUMEN Y ALINEACIÓN (Overview & Alignment)

### Propósito específico de esta Fase
Garantizar la integridad técnica y la gobernanza de datos mediante la formalización de un **Contrato de Datos (Data Contract)**. El objetivo es eliminar la ambigüedad en la estructura de las fuentes [DAT-01] a [DAT-09] antes de iniciar el modelado del MVP. Se busca automatizar la introspección de esquemas y el perfilamiento estadístico, asegurando que cualquier desviación en la calidad de los datos sea detectada preventivamente mediante una configuración centralizada y escalable.

### Tabla de Trazabilidad de la Fase
| Entregable | Objetivos Vinculados [OBJ-XX] | Requerimientos de Alto Nivel [REQ-XX] |
| :--- | :--- | :--- |
| **[DEL-03]** Data Contract Creation | **[OBJ-04]** Automatización Técnica<br>**[OBJ-05]** Neutralidad de Datos | **[MET-04]** Integración de Datos (Consolidación de fuentes)<br>**[REQ-DAT-01]** Parametrización Centralizada (config.yaml) |

---

## 2. ALCANCE ESPECÍFICO DE LA FASE (Scope)

### Qué está INCLUIDO (In Scope)
*   **[REQ-CFG-01] Orquestación por Configuración:** Implementación de `config.yaml` como única fuente de verdad para reglas de validación y parámetros de tablas.
*   **[REQ-INT-01] Introspección Dinámica (Supabase):** Identificación automática de tipos de datos y nombres de columnas de las 9 fuentes maestras. **Proceso 100% en memoria.**
*   **[REQ-STA-01] Profiling Estadístico Profundo:** Generación de estadísticas descriptivas y detección de outliers para variables numéricas, y análisis de frecuencia/peso para categóricas.
*   **[REQ-PER-01] Persistencia Triple (Consistency Loop):**
    *   **Local Dual**: `Latest` (sobrescritura) e `History` (con timestamp) para contratos y reportes.
    *   **Cloud Inmutable**: Persistencia del contrato íntegro en la tabla `sys_data_contract` de Supabase para consumo en fases posteriores.
*   **[REQ-INV-01] Política de Invalidez Atómica:** Cada ejecución exitosa de la utilidad genera un nuevo ID de ejecución (`execution_id`) e invalida estados previos.

### Qué está EXCLUIDO (Out of Scope)
*   **Pipeline Operativo**: El `builder.py` no forma parte del flujo diario de producción.
*   **Descarga de Datos**: No se permite la creación de archivos `.parquet` o `.csv` con transacciones de usuario.
*   **Validación Activa**: Esta fase define el contrato; la validación punitiva de datos ocurre en la Fase 2.

---

## 3. CASOS DE USO Y ÉPICAS (User Stories & Epics)

### Épica: Gobernanza Proactiva de Datos [EP-03]
*   **User Story 1:** Como **Data Engineer**, quiero parametrizar las validaciones (duplicados, nulos, gaps) en un archivo central para evitar cambios en el código duro vinculado a **[REQ-CFG-01]**.
*   **User Story 2:** Como **Data Scientist**, quiero un perfil estadístico inicial (outliers, medias, pesos) en el contrato para entender la salud de las variables antes de modelar, vinculado a **[REQ-STA-01]**.
*   **User Story 3:** Como **Arquitecto de Soluciones**, quiero que el contrato vigente resida en Supabase para que los servicios del MVP puedan autoconfigurarse dinámicamente, vinculado a **[REQ-PER-01]**.

---

## 4. REQUERIMIENTOS TÉCNICOS Y DE DATOS (Data & ML Requirements)

### Ingeniería de Datos y Profiling
*   **Fuentes a Procesar**: [DAT-01] a [DAT-09].
*   **Taxonomía de Validaciones ([REQ-VAL-01])**:
    *   **Integridad**: Control de filas/fechas duplicadas y columnas adicionales/faltantes.
    *   **Calidad**: Manejo de nulos, valores centinela y gaps temporales según la frecuencia definida (Diaria/Mensual/Anual).
    *   **Modelado**: Aplicación de la **Regla de Oro (X-1)**, Regla de Frescura y monitoreo de Data Drift.
*   **Reglas Personalizadas ([REQ-VAL-02])**: Soporte para validaciones lógicas cruzadas entre campos (ej. `A + B == C`).
*   **Análisis Numérico**: Cálculo de descriptivos (Media, Mediana, Desviación, Percentiles 25/75) y límites de Outliers (IQR).
*   **Análisis Categórico**: Identificación de valores únicos, frecuencia y peso relativo.

---

## 5. INGENIERÍA Y ARQUITECTURA (Engineering & Architecture [ARC-XX])

### Diseño de Componentes
*   **[ARC-09] Configuration Provider**: Motor de lectura de `config.yaml` alineado a la regla D3.5 (Cero Hardcoding).
*   **[ARC-10] Builder Utility (Out-of-Pipeline)**: Módulo `src/builder.py` que orquesta la conexión via `DBConnector`, realiza el profiling en memoria y genera los entregables.
*   **[ARC-11] Cloud State Orchestrator**: Lógica de gestión de la tabla `sys_data_contract` (manejo de flags `is_active`).

### Integración y Reportabilidad
*   **Reporte de Ejecución ([REQ-REP-01])**: Generación de `builder_report.json` con metadatos de latencia, éxito por tabla y errores capturados.
*   **Interfaz de Consumo**: Los contratos resultantes serán el input mandatorio para el `DataLoader` de la Fase 2.

---

## 6. CRITERIOS DE ACEPTACIÓN Y MÉTRICAS DE LANZAMIENTO (Release Criteria)

### Definición de Hecho (Definition of Done - DoD)
1.  **Existencia de Dual Contracts**: `data_contract.yaml` y `statistic_contract.json` generados correctamente.
2.  **Sincronización Cloud**: Tabla `sys_data_contract` actualizada con el último estado y flag `is_active` único.
3.  **Trazabilidad Completa**: Reporte `builder_report.json` disponible con latencia medida y UUID de ejecución.
4.  **Aislamiento de Código**: Cero nombres de tablas "quemados" en `src/builder.py`.

### Métricas de Lanzamiento [MET-XX]
*   **[MET-DAT-01] Cobertura de Contrato**: 100% de las tablas declaradas en el Charter deben estar perfiladas.
*   **[MET-INF-01] Latencia de Registro**: El tiempo total de introspección y persistencia (local + cloud) debe informarse en el reporte para monitoreo de performance.

---
> [!IMPORTANT]
> Este PRD ha sido refinado bajo la autoridad de un Senior AI PM, asegurando que la Etapa 1.3 sea la piedra angular de la calidad de datos para todo el proyecto "Mi Redondito".
