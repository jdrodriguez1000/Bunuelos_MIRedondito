# Project Charter: Pronóstico de Demanda "Mi Redondito"

## 1. Información General del Proyecto
| Campo | Detalle |
| :--- | :--- |
| **Nombre del Proyecto** | Sistema de Forecasting "Mi Redondito" |
| **Cliente** | Bunuelos SAS |
| **Producto Estrella** | Buñuelo |
| **Organización Ejecutora** | Sabbia Solutions & Services SAS (Triple S) |
| **Fecha de Inicio** | 11 de marzo de 2026 |
| **Horizonte de Pronóstico** | 3 meses |

---

## 2. Definición del Problema y Justificación (Business Case)
Actualmente, **Bunuelos SAS** enfrenta ineficiencias críticas en su cadena de suministro debido a un proceso de planeación de demanda altamente subjetivo.

### Problemas Actuales:
*   **Inconsistencia en el Inventario:** Frecuentes quiebres de stock (pérdida de ventas) y excesos de inventario (costos de almacenamiento y desperdicio).
*   **Alto Margen de Error:** Desfases de hasta el **25%** entre la planeación y la demanda real.
*   **Falta de Rigor Técnico:** El comité de expertos utiliza criterios variados (mes anterior, año anterior o metas impuestas) sin una metodología estadística sólida.
*   **Sesgo Gerencial:** Las cifras finales son influenciadas por negociaciones entre gerencias más que por la realidad del mercado (sesgo de optimismo o presión por metas).

---

## 3. Objetivos del Proyecto (SMART)
1.  **[OBJ-01] Optimización de Inventarios:** Reducir las **Mermas** y los **Agotados** mediante un pronóstico diario preciso.
2.  **[OBJ-02] Capacidad Prospectiva:** Implementar un módulo de **Análisis "What-If" (Simulaciones)** para evaluar el impacto de cambios en variables controlables y externas.
3.  **[OBJ-03] Reducción del Error:** Disminuir el desfase del pronóstico del 25% a un rango objetivo del **10% - 15% (MAPE)** en los primeros 6 meses de implementación.
4.  **[OBJ-04] Automatización Técnica:** Implementar una aplicación que procese datos diarios y genere pronósticos automáticos alineados con modelos matemáticos.
5.  **[OBJ-05] Neutralidad de Datos:** Reducir la influencia subjetiva en las proyecciones en un **80%**, facilitando la toma de decisiones basada en evidencias.

---

## 4. Alcance del Proyecto y Factores de Demanda
### Incluye (In-Scope):
*   **Análisis de Datos Históricos Diarios:** Procesamiento de la información base del sistema de Bunuelos SAS.
*   **Modelado de Estacionalidad y Eventos:** Integración de ciclos semanales, festivos, quincenas, primas y temporadas especiales (Novenas, Feria de las Flores, etc.).
*   **Gestión de Promociones y Marketing (Desde 2022):** Modelado de eventos 2x1 y ciclos de pauta digital (IG/FB).
*   **Módulo de Simulaciones "What-If":** Capacidad de proyectar escenarios basados en:
    *   **Elasticidad de Precio:** Impacto de aumentos o disminuciones porcentuales en el precio unitario.
    *   **Eficacia Promocional:** Escenarios de extensión o reducción de la duración de campañas 2x1 (+/- 5 o 10 días).
    *   **Sensibilidad Macroeconómica:** Efecto de inflación persistente y relación Salario Mínimo vs. Inflación.
    *   **Contingencias Climáticas:** Simulación de semanas con lluvias intensas continuas.
*   **Análisis Operacional:** Consideración de los ciclos de pedido quincenales y conversión de materia prima.
*   **Contexto Histórico y Anomalías:**
    *   **Efecto COVID-19:** Caída drástica de ventas entre el **1 de mayo de 2020 y el 31 de abril de 2021**.
    *   **Periodo de Recuperación:** Iniciado tras el fin de la anomalía COVID, con estabilización a niveles aceptables desde el **año 2023** en adelante.
*   **Variables Externas y Correlaciones (Hipótesis):**
    *   **Clima:** Exploración de la correlación entre ventas y pluviosidad (lluvia ligera vs. lluvia intensa).
    *   **Macroeconomía:** Evaluación del impacto potencial de Salario Mínimo, TRM, IPC y Desempleo.
*   **Desarrollo de Aplicación:** Herramienta tecnológica para la toma de decisiones basada en datos.

### No Incluye (Out-of-Scope):
*   **Logística Física:** No se automatiza el transporte ni la compra física de insumos.
*   **Otros Productos:** El alcance se limita exclusivamente a "El Buñuelo".

---

## 5. Dinámica Operacional e Inventarios
El sistema debe orientarse a optimizar las siguientes reglas de negocio:

### Gestión de Materia Prima (Kit de Ingredientes):
*   **Ciclos de Reabastecimiento:**
    *   **Ciclo 1:** Pedido el día 15, despacho a fin de mes para cubrir del día 1 al 14.
    *   **Ciclo 2:** Pedido el día 1, despacho el día 14 para cubrir del 15 a fin de mes.
*   **Conservación:** La materia prima en bodega se acumula y no tiene fecha de caducidad crítica para el periodo analizado.
*   **Ratio de Conversión:** 1 libra (lb) de kit equivale a la producción de 50 buñuelos.

### Gestión de Producto Terminado (Buñuelo Preparado):
*   **Vida Útil:** El buñuelo frito tiene una caducidad de **1 día**.
*   **Merma:** Los buñuelos preparados no vendidos al cierre del día representan una pérdida total.
*   **Agotados:** Ventas perdidas por falta de producto preparado disponible, independientemente de la existencia de kit en bodega.

---

## 6. Stakeholders Clave
*   **Patrocinador (Sponsor):** Gerencia General de Bunuelos SAS.
*   **Líder de Proyecto (Triple S):** Equipo de Consultoría Sabbia Solutions & Services.
*   **Comité Usuario:** Gerentes de Ventas, Producción y Finanzas (Bunuelos SAS).
*   **Usuarios Finales:** Analistas de planeación de demanda y Dueño (Tomador de decisión de fritura).

---

## 7. Riesgos y Supuestos
### Riesgos:
*   **Calidad de Datos:** Inconsistencias en los registros históricos del sistema actual.
*   **Resistencia al Cambio:** El comité actual podría preferir sus criterios subjetivos sobre el modelo.
*   **Sesgo de Merma/Agotados:** Falta de registros precisos de cuántos clientes se perdieron (agotados) en el pasado para calibrar el modelo.

---

## 8. Filosofía de Desarrollo
El proyecto se regirá bajo dos premisas fundamentales:
1.  **"Menos es más"**: Adoptar un enfoque de desarrollo por **capas incrementales**. Cada nueva funcionalidad o variable se integrará al proyecto únicamente si se demuestra que genera un valor real y tangible en la precisión de los resultados o en la toma de decisiones.
2.  **"Producción primero"**: La prioridad absoluta la tendrán los módulos de Python (`.py`) dentro de la carpeta `src/`. No se construirán notebooks para el flujo operativo; el objetivo es la automatización desde el primer día mediante código modular, reutilizable y productivo.

---

## 9. Phase-Based Roadmap
The development will follow a logical progression to ensure stability and validation of each component:

### Phase 1: Kickoff and Implementation
1.  **[DEL-01] Infrastructure and Documentation:** Environment setup and methodological foundations.
2.  **[DEL-02] Database Connection:** Establishing secure links with Supabase.
3.  **[DEL-03] Data Contract Creation:** Definition of schemas and technical validations.

### Phase 2: Minimum Viable Product (MVP) - Endogenous Variables
*Focus: Internal sales data and basic historical behavior.*
1.  **[DEL-04] MVP - Endogenous Model:** Contract validation, loading, preprocessing, EDA, Feature Engineering, Training, and Inferences.
2.  **[DEL-05] Dashboard v1:** Base visualization of forecasts.

### Phase 3: Robustness - Calendar
*Aggregation of exogenous calendar variables (holidays, weekends, semi-monthly pay periods).*

### Phase 4: Controllable Variables - Commercial & Marketing
*Integration of client-controlled variables: marketing investment and 2x1 promotions.*

### Phase 5: External Non-Controllable Variables - Macro & Weather
*Inclusion of external variables: Weather (rain), Minimum Wage, TRM, CPI (IPC), and Unemployment.*

### Phase 6: "Black Swan" Events
*Treatment of extreme and low-frequency anomalies (COVID-19 pandemic effect).*

> **Note:** The Dashboard will be an evolutionary tool, increasing its functionality and analytical depth in parallel with each executed phase.

---

## 11. Metodología Técnica de Pronóstico
Para asegurar la precisión y robustez del sistema "Mi Redondito", **Triple S** implementará la siguiente pila tecnológica y metodológica:

### Herramientas y Modelado:
*   **[ARC-01] Librería Core:** `skforecast` para la gestión de series temporales.
*   **[ARC-02] Estrategia de Forecasting:** `ForecasterAutoregDirect` (Pronóstico Directo) para capturar dependencias específicas en cada paso del horizonte.
*   **[ARC-03] Algoritmos de Entrenamiento:** Evaluación comparativa de los siguientes modelos:
    *   Lineales: `Ridge`.
    *   Basados en Árboles: `RandomForest`, `LightGBM`, `XGBoost`, `GradientBoosting`, `HistGradientBoosting`.

### Gobernanza y Versionamiento de Datos:
*   **Versionamiento de Datos (DVC):** Se implementará `DVC` (Data Version Control) para gestionar el ciclo de vida de los datasets de entrenamiento y validación.
*   **Trazabilidad Total:** Git almacenará únicamente los punteros (`.dvc`), mientras que los datos físicos residirán en almacenamiento remoto, garantizando la reproducibilidad de los modelos.

### Reglas de Negocio del Pronóstico:
1.  **Regla de Oro (Día X-1):** El modelo no utilizará la información del día actual (día X) para generar pronósticos, ya que los datos parciales pueden sesgar el resultado. La base histórica de entrenamiento y predicción será siempre hasta el día **X-1**.
2.  **Granularidad y Horizonte:**
    *   Generación de pronósticos **diarios** con un horizonte técnico de **95 días**.
    *   **Agregación Mensual:** El resultado final se agrupará por mes para facilitar la toma de decisiones estratégica.
3.  **Lógica de Visualización Trimestral:**
    *   Se entregará el pronóstico del **mes actual** + **dos meses siguientes** (completando el horizonte de 3 meses definido en el alcance).
    *   **Recorte de Incertidumbre:** Aunque se calculan 95 días, se eliminarán los días sobrantes que no completen un cuarto mes, evitando mostrar datos parciales que generen incertidumbre en el cliente.

---

## 12. Arquitectura y Origen de Datos
El proyecto se apoya en una infraestructura de datos centralizada en **Supabase (PostgreSQL)**, con información histórica desde **enero de 2017 hasta marzo de 2026**.

### Tablas y Frecuencias:

#### 1. Datos Diarios (Daily):
*   **[DAT-01]** `ventas`: Registra unidades totales, pagas y bonificadas, además de indicadores de promoción y publicidad.
*   **[DAT-02]** `clima_diario`: Información meteorológica (precipitación, probabilidad de lluvia, tipo de lluvia) para validar la hipótesis de consumo por clima.
*   **[DAT-03]** `inventario_detallado`: Tabla crítica que rastrea desde el kit inicial en bodega hasta el desperdicio (merma) y las unidades agotadas por día.
*   **[DAT-04]** `finanzas_pyme`: Precios, costos y márgenes diarios.
*   **[DAT-05]** `marketing_digital`: Inversión en redes sociales (IG/FB) y estado de campañas.
*   **[DAT-06]** `trm_diaria`: Seguimiento de la Tasa Representativa del Mercado.

#### 2. Datos Mensuales (Monthly):
*   **[DAT-07]** `desempleo_mensual`: Seguimiento de la tasa de desempleo como indicador macroeconómico.
*   **[DAT-08]** `ipc_mensual`: Índice de Precios al Consumidor para el análisis de inflación.

#### 3. Datos Anuales (Annual):
*   **[DAT-09]** `salario_minimo_anual`: Evolución del SMLV para capturar cambios en el poder adquisitivo.

---

## 13. Criterios de Éxito
El proyecto se considerará exitoso si:
1.  **[MET-01] Desempeño Técnico Superior:** El modelo seleccionado supera consistentemente a otros modelos en métricas de error (MAE, MAPE, RMSE) en el set de validación. Se considera exitoso si la métrica **MAPE (Mean Absolute Percentage Error) es inferior al 15%**.
2.  **[MET-02] Adopción Institucional:** La herramienta es adoptada por el **comité de expertos** de Bunuelos SAS como el insumo principal y oficial para sus proyecciones de demanda.
3.  **[MET-03] Impacto Operacional:** Reducción documentada de las mermas y optimización de los eventos de "Agotados" gracias a la precisión del pronóstico diario.
4.  **[MET-04] Integración de Datos:** Consolidación exitosa de todas las fuentes de Supabase en un único flujo de inferencia automatizado.
