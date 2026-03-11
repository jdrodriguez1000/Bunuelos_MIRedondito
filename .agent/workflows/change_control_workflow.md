---
description: Workflow para la gestión y registro formal de cambios en la documentación base del proyecto.
---

# WORKFLOW: Gestión de Control de Cambios (CHANGE_CONTROL)

Este flujo asegura que cualquier desviación de las especificaciones originales sea documentada y aprobada.

## Pasos del Workflow

### 1. Detección y Clasificación
- El Agente identifica si el cambio solicitado es **Menor** o **Mayor** según las [Change Control Rules](../../.agent/rules/change_control_rules.md).
- Si es Mayor, se procede con este flujo.

### 2. Creación de la Solicitud de Cambio (CR)
// turbo
Genera el documento formal en la ruta de control de cambios.
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

### 3. Solicitud de Aprobación
- El Agente presenta el impacto en el chat y solicita aprobación explícita de Triple S.

### 4. Ejecución del Efecto Dominó
- Actualizar el documento principal.
- Actualizar todos los artefactos vinculados (Charter, REQ, SPEC, IMPL) en la misma sesión.
- Incrementar versiones según el estándar (v1.0 -> v1.1).

### 5. Sincronización
- Realizar commit con el ID de la CR en el mensaje.
- Push a GitHub.
