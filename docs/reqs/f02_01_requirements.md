# PRD: Validación de Contrato de Datos (Stage 2.1)

## 1. RESUMEN Y ALINEACIÓN (Overview & Alignment)

### Propósito específico de esta Fase
Garantizar que los datos frescos provenientes de las fuentes maestras en Supabase cumplen estrictamente con los esquemas, tipos y perfiles estadísticos definidos y congelados en la Fase 01. Esta etapa actúa como un **Guardrail Operativo** (Detector de fallas preventivo) que impide que datos inconsistentes o corruptos "envenenen" el motor de pronóstico del MVP. Si el contrato no se cumple, el pipeline debe detenerse y reportar el incumplimiento.

### Tabla de Trazabilidad de la Fase
| Entregable | Objetivos Vinculados [OBJ-XX] | Requerimientos de Alto Nivel [REQ-XX] | Etiquetas de Datos [DAT-XX] |
| :--- | :--- | :--- | :--- |
| **[DEL-04.1]** Contract Validation | **[OBJ-04]**, **[OBJ-05]** | **[REQ-INV-01]**, **[MET-DAT-01]** | **[DAT-03]** |

---

## 2. ALCANCE ESPECÍFICO DE LA FASE (Scope)

### Qué está INCLUIDO (In Scope)
*   **[REQ-VAL-01] Validación Selectiva:** El proceso debe ser capaz de filtrar y validar **únicamente** la tabla `inventario_detallado` de acuerdo con la configuración de la etapa.
*   **[REQ-STR-01] Validación Estructural:** Verificación de tipos de datos, nombres de columnas y no-nulidad de los campos críticos para el cálculo de la demanda.
*   **[REQ-STA-01] Validación Estadística:** Comparación de métricas (media, desviación, mínimos y máximos) contra el `statistic_contract.json` para detectar anomalías o drift masivo.
*   **[REQ-HAS-01] Integridad de Versión:** Verificación del hash MD5 para asegurar que el contrato local no ha sido alterado manualmente vs. la versión oficial en Supabase.
*   **[REQ-WAT-01] Control de Watermark:** Gestión de punteros temporales para ejecuciones FULL, INCREMENTAL o detección de NO NEW DATA.
*   **[REQ-CFG-01] Configuración Maestro:** Gestión centralizada vía `config.yaml` para definir tablas, fases y reglas activas, permitiendo un desacoplamiento total del código.
*   **[REQ-REP-01] Reporte de Validación:** Generación de un reporte (`validation_report.json`) con persistencia doble (local y Supabase) indicando éxito o razones exactas del fallo.

### Qué está EXCLUIDO (Out of Scope) [REQ-OUT-SCOPE]
*   Validación de tablas exógenas (clima, marketing, macroeconomía, etc.) - Priorizado para Fase 3+.
*   Validación de la tabla `ventas` (se utiliza `inventario_detallado` como fuente primaria de demanda).
*   Lógica de limpieza o imputación de datos (reservado para Stage 2.3).
*   Módulo de Monitoreo y Análisis "What-If" (reservado para Fase 4+).

---

## 3. CASOS DE USO Y ÉPICAS (User Stories & Epics)

### Épica: Blindaje de Calidad Operativa [EP-06]
*   **User Story 1:** Como **System Architect**, quiero que el sistema verifique el contrato antes de cualquier proceso para evitar que cambios inesperados en la DB de producción rompan el código de ML.
*   **User Story 2:** Como **Data Scientist**, quiero un reporte claro que me diga exactamente qué columna o qué rango estadístico falló.
*   **User Story 3:** Como **Administrador de la Solución**, quiero que el pipeline cancele la ejecución si detecta que la versión del contrato local no coincide con la versión en la nube (Cloud Sync Validation).

---

## 4. REQUERIMIENTOS TÉCNICOS DE VALIDACIÓN

### Prerrequisitos de Entrada (Inputs)
*   **[REQ-INP-01] Contrato en la Nube:** Debe existir al menos un registro con `is_active = true` en la tabla `sys_data_contract` de Supabase. Este contrato es la **Única Fuente de Verdad (SSoT)** para la validación.
*   **[REQ-INP-02] Sincronización Local:** Los archivos locales `data_contract.yaml` y `statistic_contract.json` deben estar presentes para permitir la comparación de integridad (Hash).

### Fuentes del MVP para Validación
*   **Fuente Principal:** La validación se centrará exclusivamente en la tabla `inventario_detallado` **[DAT-02]**.
*   **Campos Críticos:**
    *   `fecha`: Tipo Timestamp, clave de continuidad.
    *   `demanda_teorica_total`: Variable objetivo principal (KPI).
    *   `unidades_agotadas`: Variable de apoyo para validación de demanda.
    *   `ventas_reales_totales`: Verificación de flujo.
*   **Consistencia Interna:** Validación de la regla: `demanda_teorica_total == ventas_reales_totales + unidades_agotadas`.

### Reglas de Validación (Business Rules)
1.  **Existencia**: La tabla declarada (`inventario_detallado`) debe estar accesible en Supabase.
2.  **Estructura**: No pueden faltar columnas declaradas en el contrato para esta tabla.
3.  **Tipado**: Los tipos de datos (int64, float64, object, datetime) deben ser 100% compatibles.
4.  **Continuidad**: Verificación inicial de que la data llega hasta el día **X-1** (Regla de Oro).
5.  **[REQ-VAL-03] Tipos de Ejecución por Watermark**:
    *   **FULL**: Se ejecuta si no existe un watermark previo. Valida el 100% de la historia.
    *   **INCREMENTAL**: Se ejecuta si existen datos con `fecha > watermark_latest`. Valida solo el nuevo delta.
    *   **NO NEW DATA**: Se activa si la fecha máxima de la fuente es igual al watermark. Detiene el flujo por falta de insumos frescos.

### Reportabilidad de Validación (Resultados)
*   **[REQ-OUT-01] Reporte Físico (`validator_report.json`):**
    *   **Ubicación:** `outputs/report/stage_validator/`.
    *   **Persistencia Doble:** Debe guardarse localmente y ser archivado como artefacto de ejecución.
    *   **Contenido:** Estatus global, lista de errores críticos, advertencias y latencia.
*   **[REQ-OUT-02] Persistencia en la Nube (`sys_validation_contract`):**
    *   **Destino:** Tabla `sys_validation_contract` en Supabase.
    *   **Granularidad:** Un registro por cada tabla validada (en este MVP, 1 registro para `inventario_detallado`).
    *   **Trazabilidad Total:** Cada registro **DEBE** incluir el `id_contract` (extraído del contrato activo en Supabase) para garantizar que sabemos exactamente contra qué versión de la verdad se validaron los datos.
    *   **Campos Requeridos:** `table_name`, `status` (SUCCESS/FAIL), `error_details`, `validation_timestamp`, `contract_id_ref` (UUID del contrato).
    *   **Propósito:** Servir como Flag de Auditoría para que las etapas de Carga (2.2) e Inferencia (2.7) sepan si los datos son confiables.

---

## 5. REQUERIMIENTOS DE INGENIERÍA (UX/Orquestación)

### Diseño de Arquitectura (Components)
*   **[ARC-12] Módulo Validador (`src/validator.py`)**: Motor central responsable de orquestar todas las pruebas de cumplimiento.
*   **[ARC-12.1] ContractValidator Class**: Clase principal diseñada bajo principios de robustez y *fail-fast*.
*   **[ARC-13] Integrity Report Generator**: Generador de logs de salud técnica (JSON/SQL).
*   **[ARC-14] Orquestador Principal (`main.py`)**: Punto de entrada único del sistema con soporte para modos `LOAD`, `TRAIN` y `FORECAST`.

---

## 6. ORQUESTACIÓN Y MODOS DE PIPELINE

Para el MVP, el sistema operará bajo una arquitectura dirigida por **Modos de Ejecución**, donde la validación del contrato es el "puente levante" obligatorio para cualquier proceso subsiguiente.

### Modos de Operación (main.py)
*   **[PIPE-01] MODO LOAD**: Validar (Contract) -> Cargar (Supabase).
*   **[PIPE-02] MODO TRAIN**: Validar -> Cargar -> Pre-procesar -> EDA -> Feature Engineering -> Entrenar -> Modelar.
*   **[PIPE-03] MODO FORECAST**: Validar -> Cargar -> Pre-procesar -> Feature Engineering -> Inferencia (Modelo Cargado).

### Contexto de Fase y UX de Consola (Phase Entrypoint)
*   **[REQ-ARC-15] Orquestación por Fase**: `main.py` debe recibir un parámetro obligatorio `--phase` (ej. `MVP`, `CALENDAR`).
*   **[REQ-ARC-15.1] Aislamiento de Reglas**: Solo se procesan las tablas y severidades de la fase activa.
*   **[REQ-ARC-15.3] Estándar de Ejecución (CLI)**:
    *   `python main.py --phase MVP --mode LOAD`
    *   `python main.py --phase MVP --mode TRAIN`

### Control de Flujo y Estado (Persistencia Cloud)
*   **[REQ-OUT-03] Tabla `sys_pipeline_execution`**:
    *   **Propósito**: Actuar como el **Semaforizador de Calidad** (Gatekeeper) del sistema. Cada componente posterior (Carga, Entrenamiento, Inferencia) consultará obligatoriamente el último registro de esta tabla para su fase y modo correspondientes.
    *   **Campos Definidos**:
        1.  `id` (UUID - Clave Primaria): Identificador único de cada carrera del pipeline.
        2.  `phase` (Categoría): MVP, CALENDAR, etc. (Filtro mandatorio).
        3.  `mode` (Categoría): LOAD, TRAIN, FORECAST.
        4.  `contract_id` (UUID - FK): Vínculo con el contrato de datos utilizado (`sys_data_contract`).
        5.  **`validation_status`** (Categoría): SUCCESS, WARNING, FAILED. (Este es el flag crítico de decisión).
        6.  `execution_status` (Categoría): IN_PROGRESS, COMPLETED, ABORTED.
        7.  `last_step_completed` (String): Ejemplo: `VALIDATE`, `LOAD`, `TRAIN`.
        8.  `error_summary` (Text): Descripción breve del fallo si el estatus es `FAILED`.
        9.  `timestamps`: `start_at` y `end_at`.
        10. `metadata` (JSON): Información adicional (Latencia, memoria consumida, etc.).
        11. **`watermark_start`** (Timestamp): El valor del último dato validado exitosamente en la corrida anterior.
        12. **`watermark_end`** (Timestamp): El valor máximo (`max(fecha)`) encontrado y validado en la corrida actual.
        13. **`validation_type`** (Categoría): FULL, INCREMENTAL, NO_NEW_DATA.
    *   **Regla de Continuidad**: Si el `validation_status` es `FAILED` o el `validation_type` es `NO_NEW_DATA`, la columna `execution_status` debe quedar como `ABORTED` (o `SKIPPED`) y ningún proceso subsiguiente tiene permiso de ejecución.

---

## 6. CRITERIOS DE ACEPTACIÓN Y MÉTRICAS (Release Criteria)

### Definición de Hecho (Definition of Done - DoD)
1.  **[DOD-01]** El motor valida integridad local vs. nube mediante MD5.
2.  **[DOD-02]** El sistema bloquea la ejecución ante fallos en `inventario_detallado` (Esquema/Tipado/Regla de Oro).
3.  **[DOD-03]** Doble persistencia del reporte (`json` local y `sys_validation_contract` en nube).
4.  **[DOD-04]** El orquestador `main.py` implementa correctamente los flags `--phase` y `--mode`.
5.  **[DOD-05]** El reporte JSON incluye los punteros de Watermark.

---

## 7. ESPECIFICACIONES DE VALIDACIÓN MVP (Business Case)

### Taxonomía de Resultados de Validación
Cada validación individual (Check o Regla) se clasifica como:
1.  **SUCCESS**: Validación totalmente satisfactoria.
2.  **WARNING**: Desviación no crítica; permite continuar la ejecución.
3.  **FAILED**: Fallo catastrófico; detiene la ejecución inmediatamente.

### Estatus Global del Contrato (Lógica de Decisión)
El resultado final de la validación de la tabla se determina mediante la siguiente jerarquía:
*   **ESTATUS: SUCCESS**: Se alcanza **únicamente** si el 100% de las validaciones individuales resultan en **SUCCESS**.
*   **ESTATUS: FAILED**: Se activa si **al menos una (1)** validación individual tiene el estado **FAILED**. Esta condición dispara el protocolo de parada de emergencia (Stop-Pipeline).
*   **ESTATUS: WARNING**: Se activa si existe **al menos una (1)** validación en estado **WARNING** y **ninguna (0)** validación en estado **FAILED**. Permite el paso a la Etapa 2.2 con bandera de precaución.

### Clasificación de Validaciones del MVP

| Grupo | Validación / Check | Si Falla (Severity) | Si Pasa |
| :--- | :--- | :--- | :--- |
| **Estructural (Crítico)** | **[VAL-EST-01] Existencia de Columnas** | **FAILED** | SUCCESS |
| **Estructural (Crítico)** | **[VAL-EST-02] Tipado de Datos** | **FAILED** | SUCCESS |
| **Continuidad** | `check_gold_rule` (Regla de Oro X-1) | **FAILED** | SUCCESS |
| **Continuidad** | `check_freshness` (Frescura) | **FAILED** | SUCCESS |
| **Integridad** | `allow_duplicates_rows` | WARNING | SUCCESS |
| **Integridad** | `allow_duplicates_dates` | WARNING | SUCCESS |
| **Integridad** | `allow_duplicate_columns` | WARNING | SUCCESS |
| **Calidad** | `allow_nulls` | WARNING | SUCCESS |
| **Calidad** | `check_gaps` | WARNING | SUCCESS |
| **Calidad** | `allow_sentinel_values` | WARNING | SUCCESS |
| **Calidad** | `check_drift` | WARNING | SUCCESS |
| **Reglas de Negocio** | Todas las **Custom Rules** ([BC-01] a [BC-04]) | WARNING | SUCCESS |

### Reglas de Negocio Específicas (Custom Rules)
1.  **[BC-01] Demanda Teórica**: `demanda_teorica_total == ventas_reales_totales + unidades_agotadas`
2.  **[BC-02] Positividad**: `all_fields >= 0`
3.  **[BC-03] Consistencia Física**: `abs(lbs_totales_disponibles - (lbs_iniciales_bodega + lbs_recibidas)) <= 0.01`
4.  **[BC-04] Composición de Flujo**: `ventas_reales_totales == ventas_reales_pagas + ventas_reales_bonificadas`

---
> [!IMPORTANT]
> Las validaciones marcadas como **FAILED** (Esquema, Tipado, Regla de Oro y Frescura) son los guardrails innegociables para que el MVP produzca resultados confiables.
