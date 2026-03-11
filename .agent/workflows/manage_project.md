---
description: Flujo maestro para gestionar el ciclo de vida del proyecto (Charter, PRD, Spec, Plan).
---

# /manage_project

Este workflow automatiza la creación y refinamiento de la documentación core del proyecto utilizando la habilidad `project_lifecycle_expert`.

## Pasos

1. **Identificación de Necesidad**
   Pregunta al usuario: "¿Qué acción de alto nivel deseas realizar hoy?"
   - [A] Iniciar un nuevo proyecto (Crear Project Charter).
   - [B] Generar documentación de una Fase (PRD, Spec o Plan).

2. **Ejecución de Nuevo Proyecto (Modo A: Charter)**
   Si el usuario elige [A]:
   - Saluda como el perfil dual (PM & AI PM).
   - Inicia la entrevista de la Sección 1 según la habilidad `project_lifecycle_expert`.
   - Continúa secuencialmente hasta generar el documento final.

3. **Ejecución de Documentación de Fase (Modo B, C o D)**
   Si el usuario elige [B]:
   - Pregunta la Fase (ej. 1.4) y el tipo de documento (PRD, Spec o Plan).
   - **Acción Automática:** Lee el archivo `docs/artifacts/project_charter.md` para extraer el contexto y las etiquetas de trazabilidad.
   - Si es un SPEC o PLAN, lee también los documentos previos de esa misma fase para asegurar coherencia técnica.
   - Aplica el modo correspondiente de la habilidad `project_lifecycle_expert`.

4. **Refinamiento y Cierre**
   - Presenta el borrador en la ubicación de archivo correspondiente (ej: `docs/reqs/`, `docs/specs/`, `docs/plans/`).
   - Valida con el usuario que la Matriz de Trazabilidad sea correcta.
