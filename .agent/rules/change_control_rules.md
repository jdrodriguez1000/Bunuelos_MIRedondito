# REGLAS DE CONTROL DE CAMBIOS - MI REDONDITO (CHANGE_CONTROL_RULES)

## 1. Clasificación de Cambios
- **Cambio Menor**: Correcciones ortográficas, aclaraciones de redacción o ajustes que no alteran el alcance, tiempo o costo.
    - *Acción*: Registrar en el Change Log del documento afectado. No requiere workflow extendido.
- **Cambio Mayor**: Modificaciones en objetivos `[OBJ]`, métricas `[MET]`, requerimientos `[REQ]`, fechas del roadmap `[DEL]` o exclusiones `[EXC]`.
    - *Acción*: Debe ejecutarse el `/change_control_workflow`.

## 2. Protocolo de Registro (Audit Trail)
Cualquier cambio a un documento en estado **Approved** debe seguir estas reglas:
1. **No Eliminar Historial**: No se borra contenido previo si este altera la lógica histórica. Se prefiere tachar o mover a una sección de "Obsoleto".
2. **Entrada en Change Log**: Cada edición debe generar una fila en la tabla de Registro de Cambios con:
    - `Fecha`: Formato YYYY-MM-DD.
    - `ID Elemento`: El ID específico afectado (ej. [REQ-01]).
    - `Descripción`: Explicación clara del porqué y qué cambió.
    - `Autor`: Triple S.
    - `Versión`: Nueva versión decimal (ej. de 1.0 a 1.1).

## 3. Consistencia Documental (Efecto Dominó)
Es responsabilidad del agente asegurar que si un cambio en el Project Charter afecta a un PRD, Plan de Implementación o Prueba Técnica, todos los archivos vinculados sean actualizados en la misma sesión.

## 4. Trazabilidad de Versiones
- **Borradores**: v0.X
- **Baselines Aprobados**: v1.0, v2.0, etc.
- **Revisiones Post-Aprobación**: v1.1, v1.2, etc.

## 5. Estructura de Documentación de Solicitudes (CR)
Cada cambio mayor debe generar un documento en `docs/control_changes/` siguiendo el estándar:
- **Título**: Solicitud de Cambio (Change Request) - CR_XX_XXX.
- **Secciones**: Descripción del Cambio, Impacto en Artefactos y Código, Validación y Cierre.
