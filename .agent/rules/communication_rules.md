# REGLAS DE COMUNICACIÓN ESTRATÉGICA - MI REDONDITO (COMMUNICATION_RULES)

## 1. Identificación y Control (Metadata)

*   **Título del Documento:** REGLAS DE COMUNICACIÓN (Communication Rules)
*   **Versión:** v1.0.0
*   **Estado:** Oficial / Aprobado
*   **Fecha de Creación:** 2026-03-11
*   **Trazabilidad:** Derivado de la visión de Bunuelos SAS y el estándar "Wow Factor".
*   **Objetivo:** Establecer el estándar innegociable de comunicación visual y narrativa entre el equipo técnico (Triple S) y el comité gerencial de Bunuelos SAS.

---

## 2. El Estándar "Wow Factor" (Visual & Estético)

*   **RC_COMM_001 (Identidad Visual):** Los reportes deben utilizar una paleta de colores profesional "Mi Redondito Premium". Se prohíben colores primarios básicos. Se priorizarán:
    *   **Azul Profundo**: Confianza y estabilidad estadística.
    *   **Coral Suave**: Alertas y áreas de atención (sin ser agresivo).
    *   **Arena / Gris Tenue**: Fondos y neutralidad.
*   **RC_COMM_002 (Tipografía y Diseño):** Se utilizará Markdown avanzado con jerarquía clara (H1, H2, H3), tablas comparativas y bloques de alerta (`> [!NOTE]`, `> [!IMPORTANT]`) para maximizar la legibilidad.
*   **RC_COMM_003 (Gráficas Premium):** Las figuras (en `docs/artifacts/figures/`) deben ser de alta resolución, con etiquetas en lenguaje natural. Los títulos deben ser conclusivos (ej: "Impacto del 2x1 en la demanda" en lugar de "Gráfico de barras ventas_promocion").

---

## 3. Narrativa y Tono (Lenguaje de Negocio)

*   **RC_COMM_004 (Cero Código):** Prohibido incluir nombres de librerías (Pandas, Skforecast), tecnicismos de programación o fragmentos de código en informes ejecutivos.
*   **RC_COMM_005 (Diccionario de Traducción):**
    *   *Outliers / Anomaly* -> Eventos Excepcionales / Fenómenos de Mercado.
    *   *MAPE / RMSE* -> Margen de Certidumbre / Precisión del Pronóstico.
    *   *Data Drift* -> Cambio en el Hábito del Consumidor / Evolución del Mercado.
    *   *Feature Engineering* -> Factores de Valor Identificados.
*   **RC_COMM_006 (Enfoque Decisional):** Toda conclusión debe responder: "¿Cómo afecta esto a la compra de Kit?" o "¿Cómo impacta la fritura diaria?".

---

## 4. Estructura del Informe Ejecutivo

Todo informe de cierre de fase debe seguir esta estructura:

### 4.1 ⚡ Puntos de Poder (Logros del Proyecto)
*   Resultados tangibles y validados numéricamente.
*   Impacto en la reducción de merma o optimización de inventario.

### 4.2 ⚠️ Verdades Críticas (Realidades Operativas)
*   Hallazgos que imponen acción inmediata por parte del comité.
*   Riesgos detectados en la calidad de los datos o cambios de tendencia.

---

## 5. Trazabilidad y Dual Persistence

*   **RC_COMM_007 (Nomenclatura):** Los reportes ejecutivos se llamarán `docs/executive/phase_XX_executive_latest.md`.
*   **RC_COMM_008 (Preservación):** Cada actualización genera una copia en `docs/executive/history/` con timestamp `YYMMDD_HHMMSS`.
*   **RC_COMM_009 (Vínculo Estratégico):** Cerrar siempre con recomendaciones para el Comité de Expertos vinculadas a las [Business Rules](../rules/business_rules.md).
