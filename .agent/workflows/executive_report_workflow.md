---
description: Workflow para la generación del reporte ejecutivo de alto impacto (Wow Factor) al finalizar cada fase del proyecto.
---

# WORKFLOW: Storytelling Ejecutivo (STORYTELLING_WORKFLOW)

Este workflow transforma la data técnica en valor de negocio para Bunuelos SAS.

## Pasos del Workflow

### 1. Auditoría de Hitos Técnicos
- Escanear el estado final de la fase (vía logs o base de datos).
- Extraer indicadores clave (MAPE, % de registros limpios, variables de mayor impacto).

### 2. Análisis y Visión de Datos
- Interpretar las gráficas generadas durante la fase (`docs/artifacts/figures/`).
- Validar si los hallazgos técnicos coinciden con las [Business Rules](../../.agent/rules/business_rules.md) o si hay sorpresas de mercado.

### 3. Síntesis Wow Factor
- Definir los **Puntos de Poder** (Victorias tempranas o validaciones de certeza).
- Definir las **Verdades Críticas** (Advertencias operativas basadas en datos).

### 4. Generación del Reporte Ejecutivo
- Crear el archivo `docs/executive/phase_XX_executive_latest.md`.
- Aplicar la paleta de colores y el tono directivo (Cero Código).

### 5. Doble Persistencia
// turbo
Crea la traza histórica del informe.
```powershell
$PhaseNum = if ($env:PHASE_NUM) { $env:PHASE_NUM } else { "01" } # Default a 01 si no está definido
$Timestamp = Get-Date -Format "yyMMdd_HHmmss"
$LatestPath = "docs/executive/phase_$($PhaseNum)_executive_latest.md"
$HistoryPath = "docs/executive/history/phase_$($PhaseNum)_executive_$($Timestamp).md"

if (-not (Test-Path "docs/executive/history")) { New-Item -Path "docs/executive/history" -ItemType Directory }

if (Test-Path $LatestPath) {
    Copy-Item $LatestPath $HistoryPath -Force
    Write-Host "Histórico generado en: $HistoryPath"
} else {
    Write-Warning "No se encontró el reporte latest para archivar."
}
```

---

> [!TIP]
> Al finalizar este workflow, el agente debe presentar un resumen de los hallazgos más impactantes directamente en el chat para el usuario (Triple S).
