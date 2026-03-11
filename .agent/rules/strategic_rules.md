# REGLAS ESTRATÉGICAS - MI REDONDITO (STRATEGIC_RULES)

## 1. Identificación y Control (Metadata)

*   **Título del Documento:** REGLAS ESTRATÉGICAS (Strategic Rules)
*   **Versión:** v1.0.0
*   **Estado:** Oficial / Aprobado
*   **Fecha de Creación:** 2026-03-11
*   **Trazabilidad:** Derivado de [project_charter.md](../../docs/artifacts/project_charter.md).
*   **Objetivo:** Definir las directrices de alto nivel para la toma de decisiones, la adopción del sistema y la gestión de la neutralidad en el proceso de pronóstico de **Buñuelos SAS** para el proyecto **Mi Redondito**.

---

## 2. Principios de Neutralidad y Objetividad

### 2.1 Eliminación del Sesgo Humano
*   **RE_STRAT_001 (Prioridad del Dato):** El modelo debe ser alimentado exclusivamente con datos objetivos de la base de datos (Supabase). No se permite la inyección manual de "ajustes por presentimiento" antes del procesamiento del modelo.
*   **RE_STRAT_002 (Neutralidad de Pronóstico):** Ante una discrepancia entre la cifra histórica y la opinión subjetiva de un analista, el modelo debe priorizar la tendencia estadística, documentando la diferencia si es superior al 20%.

---

## 3. Protocolo de Adopción y Comité de Expertos

### 3.1 El Rol del Panel de Expertos
*   **RE_STRAT_003 (Modelo como Referencia):** El pronóstico generado por el sistema será considerado el "Insumo Principal" para las reuniones de planeación y compra de Kit en **Buñuelos SAS**.
*   **RE_STRAT_004 (Transparencia de Decisiones):** Si el comité decide modificar una cifra del pronóstico (por ejemplo, ante un evento externo no mapeado), debe registrarse el motivo y la magnitud del cambio para realizar auditorías de "Bias" (sesgo) a futuro.

---

## 4. Gestión de Escenarios y Simulaciones

### 4.1 Toma de Decisiones "What-If"
*   **RE_STRAT_005 (Simulación Basada en Evidencia):** Las simulaciones de precios, promociones 2x1 e inflación deben usarse como herramientas de planificación estratégica, no como promesas de venta garantizada.
*   **RE_STRAT_006 (Consistencia de Escenarios):** Al ejecutar simulaciones (ej. aumento del SMLV o semanas de lluvia intensa), el analista debe utilizar los rangos de sensibilidad realistas para evitar escenarios inverosímiles que distorsionen la estrategia.

---

## 5. Mejora Continua y Gobernanza de IA

### 5.1 Evolución del Ecosistema
*   **RE_STRAT_007 (Auditabilidad):** Todo fallo técnico o desviación de MAPE > 15% debe ser revisado en un comité mensual para decidir si se requieren nuevas variables o ajustes en la ingeniería de características.
*   **RE_STRAT_008 (Propiedad de la Verdad):** La única "Fuente Única de Verdad" aceptada para el entrenamiento de los modelos es la data estructurada y validada en Supabase y el cache local procesado. No se aceptarán hojas de cálculo externas o informales.
