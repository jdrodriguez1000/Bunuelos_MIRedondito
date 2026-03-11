# REGLAS GLOBALES DEL SISTEMA (GLOBAL_RULES)

Estas reglas aplican dogmáticamente a **TODOS** los módulos, agentes, habilidades y scripts del proyecto **Bunuelos_MIRedondito**. Ninguna regla local puede sobreescribir u omitir estas directrices fundacionales.

---

## 1. Mantenimiento del Contexto y Eficiencia del Agente
- **C1.0 (Mandato del Índice):** Es OBLIGATORIO que la primera acción del agente en cada sesión sea leer el archivo `file:///c:/Users/USUARIO/Documents/Forecaster/Bunuelos_MIRedondito/index.md`. No se permite ninguna acción técnica sin haber validado el estado actual de la fase en el índice. El incumplimiento de esta regla invalida cualquier propuesta posterior.
- **C1.1 (Carga Selectiva):** No cargues jamás todas las especificaciones de forma indiscriminada. Una vez leído el índice, carga en memoria RAM únicamente los archivos específicos del módulo, fase o etapa en el que vas a trabajar.
- **C1.2 (Evitar Ruido):** Un agente desarrollando un código del módulo "Data Contract" _jamás_ considerará reglas de ventas, cobros o algoritmos de ML. Si una regla no está en tus archivos vinculados explícitamente, asúmela irrelevante.

## 2. Seguridad y Credenciales (Golden Rule)
- **S2.1 (Hardcoding Nulo):** ESTRICTAMENTE PROHIBIDO empotrar/hardcodear cadenas de conexión a base de datos, contraseñas, URLs de APIs, IPs o tokens empresariales en código `.py`, `.json` o `.yaml`.
- **S2.2 (Patrón .env):** Toda credencial secreta se consume leyendo archivos `.env` o gestores de secretos mediante `python-dotenv` y librerías `os`/`environ`.
- **S2.3 (Consistencia Temporal - DB Time):** Se prohíbe el uso de `datetime.now()` local para filtros de datos o watermarks. Toda referencia temporal operativa debe obtenerse de la base de datos (`SELECT NOW()`) para evitar desincronías entre servidores y agentes.

## 3. Filosofía "Spec-Driven Development" (Arquitectura sobre Código)
- **D3.1 (Acatamiento de Documentos):** El código (sea `.py`, `.sql`) debe ser un reflejo exacto y sumiso a los documentos técnicos de `docs/specs/` (una vez creados) y las reglas en `.agent/rules/`. Ninguna variable improvisada puede existir a costa de ignorar la Spec.
- **D3.2 (Cero Hardcoding Lógico):** ESTRICTAMENTE PROHIBIDO empotrar/hardcodear nombres de columnas, tablas, variables, rutas locales o cualquier otro parámetro de negocio dentro del código fuente. Todo comportamiento dinámico debe ser orquestado consultando el archivo maestro `config.yaml` como única fuente de parametrización.
- **D3.3 (Actualización Inversa - Reverse Sync):** Si mientras escribes código te das cuenta de que la lógica de negocio debe cambiar o descubres un caso borde clave, **DETÉN LA PROGRAMACIÓN**. Exige la actualización de la Spec o el Plan primero, antes de seguir programando, y realiza el cambio en código en un siguiente paso.
- **D3.4 (Triple Persistencia de Estado Total):** Como estándar de auditoría, cada fase del pipeline debe registrar su estado en tres frentes: un archivo `.json`/`.yaml` "latest" local, una copia histórica timestamped local, y una firma de estado en Supabase (`validation_state` o similares). Frente a un fracaso, ocultarlo omitiendo el guardado en base de datos **ESTÁ PROHIBIDO**. El error debe enviarse a DB para inmutabilidad del historial, congelando punteros si es necesario.
- **D3.5 (Jerarquía de Configuración):** El archivo `config.yaml` debe estructurarse cronológicamente por fases y etapas, y jerárquicamente de lo general a lo particular, utilizando encabezados claros. Esto garantiza que la configuración sea escalable y fácil de navegar.
- **D3.6 (Sanidad Analítica Matemática):** Todo campo en `config.yaml` diseñado como expresión libre y destinado a motores analíticos (como `pd.DataFrame.eval()` o consultas generadas en BD), debe utilizar lógicas robustas que eviten divisiones por cero (`=>` o condicionales lógicos) y deben comparar flotantes por valor absoluto en vez de depender de métodos nativos (`round()`, `ceil()`) no soportados universalmente.
- **D3.7 (Guardrailing por Ambigüedad):** Si durante el desarrollo encuentras una situación, lógica o cambio necesario que NO está contemplado en la documentación actual (`docs/specs/`, `.agent/rules/`, `.agent/skills/`), **DETÉN LA IMPLEMENTACIÓN INMEDIATAMENTE**. Debes informar al usuario sobre el cambio propuesto, proporcionar una justificación técnica o de negocio y esperar la aprobación explícitamente antes de proceder.
- **D3.8 (Sincronización Mandatoria Post-Aprobación):** Una vez recibida la autorización para un cambio no documentado, es **OBLIGATORIO** actualizar todos los archivos de documentación relacionados con la etapa en curso en las carpetas `docs/specs/`, `.agent/rules/`, `docs/artifacts/` y `.agent/skills/`, siempre y cuando aplique la actualización, antes de dar por completada la implementación.

## 4. Ingeniería de Software de Alta Calidad (Python)
- **Q4.0 (Entorno Hermético y Trazable):** Es MANDATORIO trabajar bajo un ambiente virtual (`venv`) utilizando Python 3.12+. Toda instalación de nuevas librerías debe realizarse EXCLUSIVAMENTE dentro del ambiente activo y debe reflejarse INMEDIATAMENTE en el archivo `requirements.txt` en la raíz.
- **Q4.1 (Estandarización):** Se exige adherencia total a las normas PEP 8 para legibilidad: espaciado, uso de sentencias idiomáticas y ofuscación mínima. Nombres en minúscula (snake_case) para variables y PascalCase para Clases. Todo método debe contar con type hints y docstrings explicativos.
- **Q4.2 (Pushdown y Rendimiento):** Salvo caso justificado de análisis estadísticos multivariantes no lineales, privilegia la ejecución de operaciones nativas en la base de datos (SQL Pushdown, delegación a Supabase o SQLAlchemy expressions) en lugar de importar millones de filas a un DataFrame en Pandas en la capa Python local.
- **Q4.3 (Control de Excepciones Formal):** Nunca usar bloques `except Exception: pass`. Toda falla debe ser encapsulada y mapeada a excepciones legibles con mensajes informativos, coherentes con los códigos de error dictados en las specs de los subsistemas (e.g. `ERR_ENV_001`).
- **Q4.4 (Gobernanza de Datos con DVC):** Es OBLIGATORIO versionar cualquier artefacto de datos (CSV, Parquet, Modelos PKL) mediante DVC. Se prohíbe terminantemente subir archivos binarios pesados (>1MB) a Git. El comando `dvc push` debe preceder a cualquier `git push` que involucre cambios en los datos.

## 5. Idioma y Nomenclatura
- **Nombres de Archivos y Carpetas**: Deben estar siempre en **Inglés** (ej. `data_loader.py`, `models/`, `artifacts/`).
- **Contenido de Archivos**: Todo el contenido textual, documentación, comentarios y explicaciones deben estar en **Español**.
- **Variables y Código**: Se recomienda utilizar inglés para variables y funciones por estándar de programación, pero los strings de salida al usuario deben estar en español.
