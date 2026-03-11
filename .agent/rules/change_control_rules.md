# REGLAS DE CONTROL DE CAMBIOS - MI REDONDITO (CHANGE_CONTROL_RULES)

## 1. Identificación y Control (Metadata)

*   **Título del Documento:** REGLAS DE CONTROL DE CAMBIOS (Change Control Rules)
*   **Versión:** v1.0.0
*   **Estado:** Oficial / Aprobado
*   **Fecha de Creación:** 2026-03-11
*   **Trazabilidad:** Derivado del protocolo de inmutabilidad de Triple S.
*   **Objetivo:** Garantizar que la base documental del proyecto (REQ, SPEC, IMPL) sea estable y que cualquier modificación sea justificada y trazable.

---

## 2. Inmutabilidad Documental

*   **RC_CHG_001 (Estado Aprobado):** Una vez que un documento (ej. `SPEC-F01-01`) se marca como "Oficial / Aprobado", queda prohibida su edición directa sin un proceso de Control de Cambios.
*   **RC_CHG_002 (Cero Borrado Histórico):** No se permite eliminar versiones anteriores de los requerimientos. Las evoluciones se deben registrar como nuevas versiones o adendas.

---

## 3. El Proceso de Change Request (CR)

*   **RC_CHG_003 (Justificación Obligatoria):** Todo cambio en una especificación técnica o requerimiento de negocio debe responder a:
    *   **Origen**: ¿Quién solicita el cambio? (Usuario, Hallazgo Técnico, Error).
    *   **Impacto**: ¿Cómo afecta al cronograma, presupuesto o precisión del modelo?
    *   **Riesgo**: ¿Qué puede salir mal si se aplica el cambio?
*   **RC_CHG_004 (Registro de Cambios):** Cada documento debe contar con una tabla de **Historial de Revisiones** en su sección de metadata.

---

## 4. Flujo de Aprobación

*   **RC_CHG_005 (Aprobación por el Usuario):** Los cambios que afecten el alcance del proyecto (Project Charter) deben ser aprobados explícitamente por el usuario en el chat antes de ser persistidos.
*   **RC_CHG_006 (Alineación Agente):** El Agente debe auditar si un cambio en una SPEC rompe la trazabilidad con el REQ correspondiente antes de aplicar la modificación.

---

## 5. Herramientas y Persistencia

*   **RC_CHG_007 (Snapshot de Cambio):** Antes de un cambio mayor, se recomienda realizar un commit preventivo en Git.
*   **RC_CHG_008 (Workflow de Cambio):** El uso del `/change_control_workflow` es obligatorio para modificaciones estructurales.
