# Especificación Técnica: Infraestructura y Gobernanza (Stage 1.1)

## 1. ARQUITECTURA DEL SISTEMA Y DIAGRAMA LÓGICO

### Descripción de la Arquitectura
Se ha diseñado una arquitectura de **Desarrollo Local Robusto** con **Gobernanza de Datos Híbrida**. La solución no depende de recursos en la nube pesados para el procesamiento, sino que utiliza computación local persistida mediante un sistema de versionamiento dual.

**[ARC-01] Capa de Inteligencia y Control:**
*   **Agente AI:** Operando bajo el marco de **Spec-Driven Development (SDD)**.
*   **Gobernanza:** Definida en `.agent/rules` con inmutabilidad de lógica de negocio.

**Flujo Paso a Paso:**
1.  **Entorno:** Activación de `venv` (Python 3.12.10).
2.  **Gobernanza:** Validación de `.clinerules` antes de cualquier operación.
3.  **Trazabilidad:** Registro de cambios en el `Index Maestro` y `Project Plan`.
4.  **Persistencia:** Commit de código en Git y Push de metadatos de DVC.

---

## 2. ESPECIFICACIONES DE INGENIERÍA DE DATOS (Data Pipeline)

### Orígenes y Conectores [DAT-XX]
*   **[DAT-00] Credenciales:** Implementación de conector vía `python-dotenv` para cargar variables de entorno desde `.env` **[ARC-05]**.
*   **[DAT-01-09] Acceso Supabase:** Preparación de la librería `supabase-py` para la ingesta batch en la Fase 1.2.

### Pipeline de Transformación
*   **Gestión de Datos Pesados:** Uso de `DVC` para el rastreo de archivos `.csv` y `.parquet`.
*   **Control de Versiones de Datos:** Los artefactos de datos se almacenan fuera de Git, manteniendo solo el puntero `.dvc` en el repositorio principal para asegurar la reproducibilidad del dataset.

---

## 3. DISEÑO DEL MODELO DE MACHINE LEARNING (Data Science)

### Familia de Algoritmos
*   **Base:** Aunque esta fase es de infraestructura, se pre-especifica el uso de `skforecast` **[ARC-01]** y `ForecasterDirect` **[ARC-02]**.
*   **Algoritmos Candidatos:** `Ridge`, `RandomForest`, `XGBoost`, `LightGBM` **[ARC-03]**.

### Estrategia de Validación
*   **Validación:** Se define globalmente el uso de **Backtesting** con `TimeSeriesSplit` para fases posteriores, garantizando que el diseño de la infraestructura actual soporte este tipo de iteraciones pesadas de cómputo.

---

## 4. ESPECIFICACIONES DE INTEGRACIÓN Y API [REQ-XX]

### Consumo vía Dashboard
*   **Estructura de Salida:** Se especifica que todo entregable de datos debe seguir el esquema definido en el **Contrato de Datos (Fase 1.3)**.
*   **Navegación:** El usuario interactúa con la documentación técnica a través del **Index Maestro**, que actúa como la "API de Documentación" del proyecto.

---

## 5. MLOPS, INFRAESTRUCTURA Y DESPLIEGUE

### Orquestación y Tracking
*   **Orquestación:** En esta fase, el orquestador es el **Agente AI** siguiendo el `workflow` de integración con GitHub.
*   **Tracking:** Se utilizará el sistema de archivos local y DVC para el tracking de versiones iniciales.

### Infraestructura de Desarrollo
*   **Hardware:** Cómputo basado en CPU (Windows x64).
*   **CI/CD:** Implementación de la habilidad `github_integration/SKILL.md` para automatizar commits convencionales y asegurar que ningún secreto sea filtrado.

---

## 6. MATRIZ DE DISEÑO TÉCNICO VS. PRD

| Componente Técnico | Requerimiento PRD | Etiquetas |
| :--- | :--- | :--- |
| **Ambiente Virtual (Venv)** | Aislamiento de dependencias | **[REQ-INF-01]** |
| **Gobernanza AI (.clinerules)** | Sistema de reglas agente | **[REQ-GOV-01]** |
| **Versionamiento Dual (Git/DVC)** | Trazabilidad de código y datos | **[ARC-02]** |
| **Manual de Reglas Maestro** | Centralización de lógica | **[OBJ-05]** |
| **Pattern .env** | Seguridad y gestión de secretos | **[ARC-05]** |
| **Index Maestro** | Navegación y transparencia | **[OBJ-04]** |

---
**Nota del Tech Lead:** Esta especificación asegura que el proyecto "Mi Redondito" no es solo un conjunto de scripts, sino un sistema de ingeniería escalable y reproducible.
