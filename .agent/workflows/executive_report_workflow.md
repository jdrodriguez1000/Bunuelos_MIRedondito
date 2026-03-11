---
description: Workflow para la generación y archivo de reportes ejecutivos de cierre de fase.
---

# WORKFLOW: Generación de Reporte Ejecutivo (EXECUTIVE_REPORT)

Este flujo automatiza la creación de informes de alto nivel para el comité de Bunuelos SAS, garantizando el estándar "Wow Factor".

## Pasos del Workflow

### 1. Preparación de Directorios
// turbo
Asegura que la estructura de persistencia dual existe.
```powershell
$PathLatest = "docs/executive"
$PathHistory = "docs/executive/history"
if (-not (Test-Path $PathLatest)) { New-Item -Path $PathLatest -ItemType Directory }
if (-not (Test-Path $PathHistory)) { New-Item -Path $PathHistory -ItemType Directory }
```

### 2. Generación del Contenido
- El Agente revisa el `IMPL-F01-XX` de la fase terminada.
- Traduce las métricas técnicas a lenguaje de negocio.
- Redacta el informe siguiendo la estructura de **Puntos de Poder** y **Verdades Críticas**.

### 3. Persistencia Dual
// turbo
Guarda el reporte en `latest` y crea la copia histórica.
```powershell
$Phase = "01" # Ajustar según la fase actual
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$FileName = "phase_$($Phase)_executive_latest.md"
$HistoryName = "$($Timestamp)_phase_$($Phase)_executive.md"

# El contenido se genera dinámicamente
# $Content = [Contenido generado por el Agente]
# Set-Content -Path "docs/executive/$FileName" -Value $Content
# Copy-Item -Path "docs/executive/$FileName" -Destination "docs/executive/history/$HistoryName"
```

### 4. Notificación al Usuario
- Informar al usuario que el reporte ha sido generado y está listo para ser presentado al Comité de Expertos.
