# REGLAS TÉCNICAS - MI REDONDITO (TECHNICAL_RULES)

## 1. Identificación y Control (Metadata)

*   **Título del Documento:** REGLAS TÉCNICAS (Technical Rules)
*   **Versión:** v1.0.0
*   **Estado:** Oficial / Aprobado
*   **Fecha de Creación:** 2026-03-11
*   **Trazabilidad:** Derivado de [project_charter.md](../../docs/artifacts/project_charter.md).
*   **Objetivo:** Establecer los estándares técnicos de procesamiento, modelado y validación para el ecosistema de pronóstico de **Buñuelos SAS** para el proyecto **Mi Redondito**.

---

## 2. Protocolo de Procesamiento de Datos (Data Engineering)

### 2.1 Upsampling y Alineación Temporal
Para garantizar que todas las series de tiempo tengan la misma granularidad diaria requerida por `skforecast`:

*   **RT_DATA_001 (Upsampling Mensual):** Los datos con frecuencia mensual (ej. IPC, desempleo) deben propagarse a frecuencia diaria. Se utilizará el método de **propagación (Forward Fill)** desde el primer día del mes hasta el último, manteniendo el valor constante durante todo el periodo.
*   **RT_DATA_002 (Upsampling Anual):** Los datos con frecuencia anual (ej. salario mínimo) deben propagarse a frecuencia diaria. El valor se mantendrá constante desde el 1 de enero hasta el 31 de diciembre de cada año.
*   **RT_DATA_003 (Manejo de GAPs):** No se permiten huecos en las series de tiempo una vez realizado el upsampling. Cualquier fecha faltante tras la alineación debe ser reportada como un error crítico de integridad.

### 2.2 Ingeniería de Características (Features)
*   **RT_DATA_004 (Codificación Categórica):** Las variables de texto o categóricas (festivos, promociones, tipo de clima) deben convertirse en variables binarias (One-Hot Encoding) o flags de 0/1.
*   **RT_DATA_005 (Tratamiento COVID):** El periodo atípico definido en el Project Charter (01/05/2020 - 30/04/2021) debe ser marcado mediante un flag binario `is_covid` para que el modelo pueda discernir el cambio estructural de la demanda.
*   **RT_DATA_006 (Variables de Marketing):** Se debe crear una variable flag para la pauta publicitaria, considerando que esta inicia 20 días antes de la promoción y termina el día 25 del mes en que finaliza la misma.

### 2.3 Gobernanza de Datos (DVC)
*   **RT_DATA_007 (Versionamiento de Datasets):** Todo dataset crudo extraído de Supabase y todo dataframe preprocesado intermedio debe ser versionado con `DVC`.
*   **RT_DATA_008 (Snapshot de Entrenamiento):** Antes de iniciar un entrenamiento (`RT_ML_004`), se debe ejecutar `dvc commit` para congelar el estado exacto de los datos utilizados, garantizando la reproducibilidad del experimento.
*   **RT_DATA_009 (Integridad de Punteros):** Los archivos `.dvc` resultantes deben ser incluidos en el mismo commit de Git que el código que procesó dichos datos.

---

## 3. Protocolo de Modelado (Machine Learning)

### 3.1 Arquitectura del Forecaster
*   **RT_ML_001 (Estrategia):** Uso mandatorio de `ForecasterAutoregDirect` para series múltiples o univariantes según aplique el diseño final.
*   **RT_ML_002 (Modelos):** Evaluación obligatoria de la terna: Ridge, RandomForest, LightGBM, XGBoost, GradientBoosting e HistGradientBoosting.
*   **RT_ML_003 (Horizonte de Predicción):** El horizonte de salida (`steps`) será siempre de **95 días**.

### 3.2 Entrenamiento y Backtesting
*   **RT_ML_004 (Ventana de Validación):** Se utilizará una estrategia de **Time Series Cross-Validation** (Rolling Window) para evaluar la estabilidad del modelo en diferentes periodos del año.
*   **RT_ML_005 (Métrica de Selección):** El modelo ganador será aquel que minimice el **MAPE (Mean Absolute Percentage Error)**. El éxito técnico se define únicamente si **MAPE < 15%**.
*   **RT_ML_006 (Overfitting):** Se deben monitorear las brechas entre el error de entrenamiento y el de test. Una diferencia superior al 10% en MAPE se considerará sobreajuste.

---

## 4. Protocolo de Inferencia y Salida (Operational)

### 4.1 Regla de Oro de Inferencia
*   **RT_OPS_001 (Información Disponible):** La ejecución del pronóstico en el día `X` solo podrá utilizar datos validados hasta el día `X-1`. No se permite el uso de información parcial del día en curso.

### 4.2 Post-procesamiento de Resultados
*   **RT_OPS_002 (Consolidación Mensual):** El resultado diario debe sumarse para generar el pronóstico de los meses completos siguientes.
*   **RT_OPS_003 (Truncamiento de Incertidumbre):** Si el horizonte de 95 días incluye días de un mes incompleto al final, esos días deben ser descartados del reporte final al cliente para evitar proyecciones incompletas que generen incertidumbre.

---

## 5. Protocolo de Calidad y Monitoreo (MLOps)

### 5.1 Detección de Drift (Fases 2+)
*   **RT_MON_001 (Umbrales de Drift):** Se utilizará una sensibilidad Z-Score de 2.0 y 3.0 para disparar alertas de advertencia (Warnings). El Drift significativo nunca debe bloquear la inferencia, pero sí debe registrarse en los logs de auditoría.
*   **RT_MON_002 (Re-entrenamiento):** Un incremento sostenido del MAPE por encima del 15% durante 2 semanas consecutivas disparará un proceso de auditoría de modelo y re-entrenamiento forzado.
