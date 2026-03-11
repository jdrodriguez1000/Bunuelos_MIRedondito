---
description: Gestión profesional de solicitudes de cambio para documentos aprobados.
---

# WORKFLOW: Gestión de Control de Cambios (CHANGE_CONTROL)

Este workflow garantiza que cualquier modificación al proyecto sea trazable, aprobada y consistente en toda la documentación (Efecto Dominó).

## Pasos del Workflow

### 1. Recepción y Clasificación
- **Acción**: Identificar la solicitud del usuario y clasificarla (Menor vs Mayor).
- **Herramienta**: Consultar las [Change Control Rules](../../.agent/rules/change_control_rules.md).

### 2. Análisis de Impacto (Sólo Cambios Mayores)
- **Acción**: Realizar un escaneo de los documentos actuales para identificar dependencias.
- **Salida**: Informar al usuario: "¿Si cambiamos [X], sabías que esto afecta a [Y] y [Z]?".

### 3. Creación de la Solicitud de Cambio (CR)
// turbo
Genera el documento formal en la ruta de control de cambios para auditoría.
```powershell
$PathCC = "docs/control_changes"
if (-not (Test-Path $PathCC)) { New-Item -Path $PathCC -ItemType Directory }

$CR_ID = "CR_$(Get-Date -Format 'MM_dd_HHmm')"
$PathCR = "$PathCC/$($CR_ID).md"

$CR_Template = @"
# Solicitud de Cambio (Change Request) - $($CR_ID)
## Proyecto: Mi Redondito - Bunuelos SAS
### [Título descriptivo del cambio]

**Estado**: PENDIENTE
**Fecha**: $(Get-Date -Format 'yyyy-MM-dd')
**Autor**: Antigravity (AI Agent)

---

## 1. DESCRIPCIÓN DEL CAMBIO
[Describir qué cambia y por qué. Referenciar IDs afectados ej. REQ-F01-01]

---

## 2. IMPACTO EN ARTEFACTOS Y CÓDIGO
| Artefacto | Versión | Ajuste |
| :--- | :--- | :--- |
| [Ej. project_charter.md] | [vX.X] | [Descripción] |

---

## 3. VALIDACIÓN Y CIERRE
[Criterios para dar por cerrado el cambio]
---
**Autoridad de Configuración**: Change Manager PM (Antigravity)
"@

New-Item -Path $PathCR -Value $CR_Template -ItemType File
Write-Host "CR creada en: $PathCR"
```

### 4. Actualización del Project Charter (Change Log)
- **Acción**: Ir a la sección "Registro de Cambios" del [Project Charter](../../docs/artifacts/project_charter.md).
- **Edición**: Agregar la nueva entrada con la fecha de hoy, autor "Triple S" y nueva versión.
- **Actualización**: Modificar el elemento específico (`[REQ]`, `[OBJ]`, etc.) dentro del Charter.

### 5. Propagación en Cascada
- **Acción**: Actualizar documentos secundarios afectados (PRDs, SPECs, Implement Plans).
- **Edición**: Actualizar estos documentos e incrementar sus versiones (v1.0 -> v1.1).

### 6. Verificación de Trazabilidad
- **Acción**: Validar que la **Matriz de Trazabilidad** al final del Project Charter siga siendo correcta.
- **Edición**: Ajustar la tabla de trazabilidad si se agregaron o eliminaron requerimientos o entregables.

### 7. Confirmación y Sincronización
- **Acción**: Mostrar al usuario un resumen de los archivos actualizados.
- **Sincronización**: Realizar commit en Git con el ID de la CR y push a GitHub.
