---
description: Workflow para la gestión y registro formal de cambios en la documentación base del proyecto.
---

# WORKFLOW: Gestión de Control de Cambios (CHANGE_CONTROL)

Este flujo asegura que cualquier desviación de las especificaciones originales sea documentada y aprobada.

## Pasos del Workflow

### 1. Detección de Necesidad de Cambio
- El Agente identifica que una tarea del `IMPL-PLAN` no puede cumplirse según la `SPEC` actual o el usuario solicita una modificación.

### 2. Creación del Registro de Cambio (CR)
// turbo
Genera una entrada en el log de control de cambios.
```powershell
$PathChangeLog = ".agent/change_control/change_log.md"
if (-not (Test-Path ".agent/change_control")) { New-Item -Path ".agent/change_control" -ItemType Directory }

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$ChangeEntry = @"
---
### [CR-$(Get-Date -UFormat %Y%m%d%H%M%S)] - $($Timestamp)
*   **Documento Afectado:** [Nombre del Documento]
*   **Descripción del Cambio:** [Describir qué cambia]
*   **Razón:** [Hallazgo técnico / Solicitud de usuario]
*   **Estado:** PENDIENTE DE APROBACIÓN
---
"@

if (-not (Test-Path $PathChangeLog)) {
    New-Item -Path $PathChangeLog -Value "# LOG DE CONTROL DE CAMBIOS`n`n" -ItemType File
}
Add-Content -Path $PathChangeLog -Value $ChangeEntry
```

### 3. Solicitud de Aprobación
- El Agente presenta la justificación técnica al usuario en el chat.
- Se debe explicar el impacto en las métricas **[MET-XX]** u objetivos **[OBJ-XX]**.

### 4. Ejecución del Cambio
- Una vez aprobado, se actualiza el documento afectado.
- Se debe incrementar la versión en la metadata del documento (ej. v1.0.0 -> v1.1.0).
- Se actualiza el estado en el `change_log.md` a **APROBADO**.

### 5. Sincronización
- Realizar commit en Git con el prefijo `fix:` o `refactor:` según corresponda.
