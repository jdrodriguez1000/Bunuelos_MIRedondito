---
name: github_integration
description: Habilidad para administrar el control de versiones local, orquestar commits convencionales y enlazar o actualizar un repositorio remoto en GitHub.
---

# Skill: Integración y GitOps (GitHub)

Esta habilidad permite al agente gestionar el ciclo de vida del código y la documentación, asegurando que los avances de **Buñuelos SAS** estén respaldados y versionados de forma segura en el proyecto **Mi Redondito**.

## 🛠️ 1. Capacidades Principales

### A. Gestión de Repositorio Local y Data Control
- Audita el estado de los archivos (`git status` y `dvc status` si aplica).
- Aplica limpiezas proactivas y asegura la segregación entre flujos de código y datos.
- Sincroniza punteros `.dvc` con el estado del dataset local (cuando se implemente DVC).

### B. Versionamiento Estructurado
- Crea ramas orientadas a objetivos específicos alineados con las fases del [Project Plan](../../../docs/artifacts/project_plan.md).
- Usa prefijo `data:` para commits que actualizan versiones de datasets pesados.
- Redacta mensajes de commit bajo el estándar **Conventional Commits** (`feat`, `fix`, `docs`, `data`) en español.

### C. Operación Remota (GitHub)
- Interactúa con el servidor MCP `remote-github` para operaciones de PR y Sincronización.
- **Orquestación S3/Remote**: Ejecuta `dvc push` (o comandos de sincronización de datos definidos) proactivamente antes del push de Git.

## 📋 2. Procedimiento de Seguridad Pre-Push
1.  **Escaneo de Secretos**: Revisa visualmente archivos en staging para detectar credenciales (Regla G1.2).
2.  **Protección de Data-Heavies**: Garantiza que archivos grandes no se suban por Git accidentalmente (DVC Check).
3.  **Aislamiento de Cache**: Verifica que la carpeta `.dvc/cache/` (o similares) esté estrictamente excluida de Git.

## ⚠️ Restricciones
- **PROHIBIDO** el comando `git push origin main` salvo en el commit de inicialización.
- **PROHIBIDO** ignorar conflictos de merge; si existen, el agente debe detenerse y pedir intervención.
