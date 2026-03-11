# PRD: Infraestructura y Gobernanza (Stage 1.1)

## 1. RESUMEN Y ALINEACIÓN (Overview & Alignment)

### Propósito específico de esta Fase
Establecer los cimientos técnicos y metodológicos del proyecto "Mi Redondito". Esta fase no entrega un modelo, sino el "sistema de reglas" y el "ecosistema de ejecución" necesarios para que el equipo de Triple S pueda desarrollar de forma trazable, segura y bajo la filosofía de Spec-Driven Development (SDD).

### Tabla de Trazabilidad de la Fase
| Entregable | Objetivos Vinculados | Requerimientos de Alto Nivel |
| :--- | :--- | :--- |
| **[DEL-01]** Infraestructura y Gobernanza | **[OBJ-04]** Automatización Técnica<br>**[OBJ-05]** Neutralidad de Datos | **[REQ-INF-01]** Entorno v3.12+<br>**[REQ-GOV-01]** Sistema de Reglas Agente |

---

## 2. ALCANCE ESPECÍFICO DE LA FASE (Scope)

### Qué está INCLUIDO (In Scope)
*   Configuración del entorno de desarrollo local (Python 3.12.10 y venv).
*   Protocolos de gobernanza del Agente (Reglas Globales, Técnicas, de Negocio).
*   Configuración de herramientas de versionamiento dual: Git (Código) y DVC (Datos).
*   Formalización de la metodología SDD (Requerimientos, Especificaciones, Planes).
*   Definición de habilidades (Skills) para tareas críticas (GitHub Integration).

### Qué está EXCLUIDO (Out of Scope)
*   Conexión física a la base de datos (corresponde a [DEL-02]).
*   Carga de datos históricos o preprocesamiento.
*   Diseño de interfaces de usuario o Dashboards.

---

## 3. CASOS DE USO Y ÉPICAS (User Stories & Epics)

### Épica: Gestión de Entorno y Gobernanza
*   **User Story 1:** Como Desarrollador, quiero un ambiente virtual aislado para asegurar que las dependencias sean consistentes y reproducibles. vinculada a **[REQ-INF-01]**.
*   **User Story 2:** Como Project Manager, quiero un sistema de reglas escrito para que el Agente AI no cometa errores de proactividad o borre información sin permiso. vinculada a **[REQ-GOV-01]**.
*   **User Story 3:** Como Data Engineer, quiero tener DVC configurado desde el día 1 para evitar que archivos binarios pesados contaminen el repositorio de Git. vinculada a **[ARC-02]**.

---

## 4. REQUERIMIENTOS TÉCNICOS Y DE DATOS (Data & ML Requirements)

### Target y Granularidad
*   N/A para esta fase. La infraestructura soporta granularidad **diaria** para fases futuras.

### Requerimientos de Ingeniería de Datos
*   **Control de Versiones de Datos:** Implementación mandatoria de `DVC` para datasets.
*   **Gestión de Dependencias:** Registro automático en `requirements.txt` tras cada instalación de librería.

### Estrategia de Modelado
*   N/A. Se establece que el código productivo residirá en `src/` siguiendo la premisa "Producción primero".

---

## 5. INGENIERÍA Y ARQUITECTURA [ARC-XX]

### Infraestructura
*   **[ARC-04] Entorno de Ejecución:** Windows 11 con PowerShell como terminal principal.
*   **[ARC-05] Gestión de Secretos:** Implementación de patrón `.env` para evitar *hardcoding* de credenciales.

### Integración / UX
*   **Index Maestro:** Navegación centralizada vía Markdown para que el usuario pueda auditar el avance de forma no técnica.

---

## 6. CRITERIOS DE ACEPTACIÓN Y MÉTRICAS DE LANZAMIENTO (Release Criteria)

### Definición de Hecho (Definition of Done)
1.  Archivo `.clinerules` configurado con mandatos de proactividad.
2.  Index Maestro funcional y con enlaces correctos a todos los documentos de gobernanza.
3.  Git y DVC inicializados en la raíz del proyecto.
4.  Estructura de documentación `REQ/SPEC/IMPL` generada y alineada.

### Métricas Técnicas [MET-XX]
*   **[MET-INF-01]** 100% de las dependencias base (`pandas`, `skforecast`, `dvc`) instaladas y reportadas en `requirements.txt`.
*   **[MET-GOV-01]** 0 errores de escritura no autorizada detectados en el paso a producción.

### Métricas de Negocio / Adopción
*   Confirmación del Sponsor sobre la claridad del Roadmap y las Reglas de Negocio inyectadas en el sistema.
