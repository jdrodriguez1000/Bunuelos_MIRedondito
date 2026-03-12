---
description: Sincronización segura y ordenada con el repositorio de GitHub siguiendo las reglas globales y de integración.
---

# WORKFLOW: Sincronización con GitHub (GITHUB_SYNC)

Este flujo garantiza que el conocimiento y el código generado para el proyecto **Mi Redondito** residan de forma segura en la nube, siguiendo estándares profesionales de ingeniería.

## Pasos del Workflow

### 1. Saneamiento Pre-Sincronización
// turbo
Limpia archivos temporales y residuales en el entorno Windows.
```powershell
# Buscar y eliminar archivos residuales comunes
Get-ChildItem -Path . -Include *.log, *.tmp, *.pyc, __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
```

### 2. Blindaje de Seguridad (`.gitignore`)
// turbo
Verifica o crea el escudo de archivos para evitar fugas de secretos o datos pesados.
```powershell
$GitIgnoreContent = @"
# Secrets
.env

# Python
__pycache__/
*.pyc
venv/
env/
.venv/
.pytest_cache/

# DVC (Data Version Control)
.dvc/cache/
.dvc/tmp/
.dvc/config.local

# Agent History
.agent/artifacts/test_history/
.agent/artifacts/history/

# Data (Managed by DVC or excluded)
data/
*.csv
*.parquet
"@

if (-not (Test-Path .gitignore)) {
    New-Item -Path .gitignore -Value $GitIgnoreContent -ItemType File
}
```

### 3. Orquestación del Repositorio (Git + MCP)
3.1. Ejecutar `git init` si no existe el repositorio local.
3.2. **Acción MCP**: Si no existe el remoto, usar `mcp_remote-github_create_repository` con el nombre `Bunuelos_MIRedondito`.
3.3. Vincular local con remoto: `git remote add origin https://github.com/[PROPIETARIO]/Bunuelos_MIRedondito.git`.

### 4. Ciclo de Versionamiento Dual (Git + DVC) con Validación
// turbo
Valida la calidad localmente y, si es satisfactoria, sincroniza datos y código.

```powershell
# 4.0 Validación de Calidad Obligatoria
Write-Host "Iniciando validación de calidad antes de sincronizar..." -ForegroundColor Cyan
/test_pipeline   # Ejecuta el flujo de pruebas existente

if ($LASTEXITCODE -ne 0) {
    Write-Error "Las pruebas FALLARON. La sincronización se ha abortado para proteger el repositorio."
    exit $LASTEXITCODE
}

Write-Host "Pruebas exitosas. Procediendo con la sincronización..." -ForegroundColor Green

# 4.1 Sincronización de Datos (DVC - Si aplica)
# dvc add data/  
# dvc push       

# 4.2 Sincronización de Código y Punteros (Git)
# Usar rama descriptiva según fase actual del Project Plan
git checkout -b feature/fase-01-infrastructure
git add .
git status # Revisar que no haya secretos (Regla G1.2)
git commit -m "feat: implementacion inicial de gobernanza y protocolos de infraestructura"

# 4.3 Push Remoto
git push -u origin feature/fase-01-infrastructure
```

---

> [!CAUTION]
> Asegúrate de que las credenciales de GitHub estén configuradas en tu terminal de Windows (vía Git Credential Manager o SSH) antes de ejecutar el Paso 4.
