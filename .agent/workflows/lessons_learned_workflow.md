---
description: Workflow para la captura y sistematización de aprendizajes del proyecto.
---

# WORKFLOW: Gestión de Lecciones Aprendidas (LEARN_FLOW)

Este flujo se ejecuta al final de cada fase o después de resolver un incidente crítico.

## Pasos del Workflow

### 1. Auditoría de Experiencia
Analizar los últimos logs de ejecución y feedbacks del usuario.
- ¿Hubo retrabajos?
- ¿Se malinterpretó alguna regla de negocio?
- ¿Qué herramienta funcionó excepcionalmente bien?

### 2. Clasificación del Hallazgo
Categorizar según [Lessons Learned Rules](../../.agent/rules/lessons_learned_rules.md) (Technical, Business, Process).

### 3. Registro en el Log
Actualizar el archivo `docs/lessons_learned/lessons_learned_log.md`.
// turbo
```powershell
$LogPath = "docs/lessons_learned/lessons_learned_log.md"
if (-not (Test-Path "docs/lessons_learned")) { New-Item -Path "docs/lessons_learned" -ItemType Directory }
if (-not (Test-Path $LogPath)) { New-Item -Path $LogPath -Value "# LOG DE LECCIONES APRENDIDAS - MI REDONDITO`n`n" -ItemType File }

# El Agente añadirá la entrada estructurada usando sus herramientas de edición.
```

### 4. Propagación de Conocimiento
Si la lección aprendida implica un cambio en las Reglas Globales o Técnicas:
- Activar el `/change_control_workflow` para actualizar las reglas correspondientes.

### 5. Cierre de Ciclo
Confirmar al usuario que el aprendizaje ha sido institucionalizado.
