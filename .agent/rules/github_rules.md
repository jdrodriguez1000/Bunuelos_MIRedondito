# REGLAS DE INTEGRACIÓN CON GITHUB (GITHUB_RULES)

Estas reglas definen el estándar de versionamiento y despliegue del código hacia los repositorios de GitHub para el proyecto **Mi Redondito** (Buñuelos SAS).

---

## 1. CONTROL DE SECRETOS, LIMPIEZA Y EXCLUSIONES
*   **G1.0 (Limpieza Pre-Commit Obligatoria):** Antes de añadir archivos al índice (`git add`), es OBLIGATORIO auditar activamente el árbol de directorios para identificar y ELIMINAR archivos temporales, logs locales o archivos de diagnóstico.
*   **G1.1 (.gitignore Estricto):** Es MANDATORIO actualizar y verificar el archivo `.gitignore` antes de cualquier operación de Git. ESTRICTAMENTE PROHIBIDO hacer commit o push de:
    *   Archivos `.env` (Secretos y Credenciales).
    *   Entornos virtuales (`venv/`, `env/`, `.venv/`).
    *   Cachés de Python (`__pycache__/`, `.pytest_cache/`).
    *   Archivos de base de datos local o temporales de Excel/CSV no validados.
    *   Documentación temporal o archivos de respaldo.
*   **G1.2 (Cero Credenciales):** Si se detecta un token o contraseña en el area de preparación (*staging*), debe retirarse inmediatamente con `git rm --cached`.
*   **G1.3 (Segregación de Datos Pesados):** ESTRICTAMENTE PROHIBIDO usar `git add` en archivos de datos pesados (CSV, Parquet, Modelos Binarios). Estos deben ser gestionados por un sistema de versionamiento de datos (como DVC) o mantenidos fuera de Git.

## 2. ESTRUCTURA DE COMMITS (Conventional Commits)
*   **G2.1 (Atomicidad):** Los commits deben ser pequeños y enfocados en una sola tarea.
*   **G2.2 (Sintaxis Estándar):**
    *   `feat: [Descripción]` -> Nuevas funcionalidades o modelos.
    *   `fix: [Descripción]` -> Corrección de bugs o lógica.
    *   `docs: [Descripción]` -> Actualización de reglas, specs o planes en `.agent/` o `docs/`.
    *   `refactor: [Descripción]` -> Mejora de código sin cambiar funcionalidad.
    *   `chore: [Descripción]` -> Configuración, dependencias o mantenimiento (ej. `requirements.txt`).
    *   `data: [Descripción]` -> Actualización de metadatos o versiones de datos.
*   **G2.3 (Idioma):** Los mensajes de commit deben escribirse en **Español** para mantener la coherencia con la documentación del proyecto.

## 3. FLUJO DE RAMAS (Branching Strategy)
*   **G3.1 (Rama Principal):** La rama por defecto será `main` (o `master` según se configure inicialmente).
*   **G3.2 (Uso de Ramas):** Se prohíbe el push directo a la rama principal para cambios significativos. Se deben usar ramas descriptivas:
    *   `feature/nombre-funcionalidad`
    *   `bugfix/nombre-error`
    *   `docs/actualizacion-gobernanza`

## 4. PULL REQUESTS Y SINCRONIZACIÓN
*   **G4.1 (Trazabilidad):** Toda integración a la rama principal debe pasar por una revisión de los archivos afectados para asegurar que no se sube información sensible o innecesaria.
*   **G4.2 (Sincronización Total):** Un commit que altere la lógica de procesamiento debe asegurar que los archivos de configuración (`config.yaml`) o dependencias (`requirements.txt`) estén actualizados y sincronizados.
