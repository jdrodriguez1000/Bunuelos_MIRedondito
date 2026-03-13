# IMPL: Plan de Implementación - Validación de Contrato (Stage 2.1)

## 1. ALINEACIÓN Y TRAZABILIDAD [IMPL-01]
Este plan detalla la ejecución técnica para activar el **Guardrail de Calidad** del sistema "Mi Redondito". Asegura que ninguna fase de carga o entrenamiento ocurra sin una validación previa exitosa.

| Dimensión | Referencia de Trazabilidad |
| :--- | :--- |
| **Objetivos de Negocio** | **[OBJ-04]**, **[OBJ-05]** |
| **Entregable Charter** | **[DEL-04]** MVP - Endogenous Model |
| **Requerimientos PRD** | **[REQ-VAL-01]**, **[REQ-HAS-01]**, **[REQ-WAT-01]**, **[REQ-OUT-03]** |
| **Componentes SPEC** | **[ARC-12]**, **[ARC-13]**, **[ARC-14]**, **[ARC-15]** |

---

## 2. CRONOGRAMA Y EQUIPO (Sprint Plan) [IMPL-02]
La ejecución se concentrará en un **Micro-Sprint de 4 ciclos de trabajo (2 días totales)**.

| Rol | Responsabilidad | Carga Horaria |
| :--- | :--- | :--- |
| **Principal ML Engineer (Tech Lead)** | Diseño de lógica vectorizada y validación de Watermarks. | 12h |
| **MLOps Engineer** | Orquestación CLI, integración cloud y persistencia. | 8h |
| **QA Automation** | Suite de pruebas de contrato y validación de seguridad. | 4h |

---

## 3. RUTA CRÍTICA (Serialización de Dependencias) [IMPL-03]
Para garantizar la integridad del sistema, las tareas deben seguir este orden estricto:
0.  **[SETUP]**: Configuración de `config.yaml` y creación de tablas `sys_validation_contract` / `sys_pipeline_execution`.
1.  **[SEGURIDAD]**: Validación de Integridad del Contrato (MD5). No se lee data si el contrato está alterado.
2.  **[CONTROL]**: Detección de Watermarks en Supabase para definir el modo (`FULL` / `INC`).
3.  **[PROCESAMIENTO]**: Ejecución de reglas de negocio vectorizadas sobre la tabla `inventario_detallado`.
4.  **[CIERRE]**: Registro de auditoría y activación del semáforo en `sys_pipeline_execution`.

---

## 4. BACKLOG Y WBS (Work Breakdown Structure) [IMPL-04]

### [Ciclo 1] Setup de Infraestructura & Seguridad (Día 1 - AM)
| ID Tarea | Tarea Técnica | Tag Trazabilidad | Entregable |
| :--- | :--- | :--- | :--- |
| **[TASK-INF-01]** | Segmentación de fases y tablas en `config.yaml`. | **[REQ-CFG-01]** | `config.yaml` |
| **[TASK-INF-02]** | Creación física de tablas de auditoría en Supabase. | **[REQ-OUT-02/03]** | Supabase Migration |
| **[TASK-VAL-01]** | Implementar `IntegrityChecker` (MD5 local vs Cloud). | **[REQ-HAS-01]** | `src/validator.py` |
| **[TASK-VAL-02]** | Desarrollar `WatermarkManager` (Lógica FULL/INC/SKIP). | **[REQ-WAT-01]** | `src/validator.py` |
| **[TASK-VAL-03]** | Implementar validación de tipos y esquema (Gate 1). | **[REQ-STR-01]** | `src/validator.py` |
| **[TASK-VAL-04]** | Lógica de pre-filtrado por flag `enabled`. | **[REQ-SELECT-01]** | `src/validator.py` |

### [Ciclo 2] Lógica de Negocio y Regras [BC-XX] (Día 1 - PM)
| ID Tarea | Tarea Técnica | Tag Trazabilidad | Entregable |
| :--- | :--- | :--- | :--- |
| **[TASK-BC-01]** | Regla de Demanda Teórica (Suma vectorizada). | **[REQ-VAL-01]** | `src/validator.py` |
| **[TASK-BC-02]** | Regla de Ventas Totales vs Pagas/Bonificadas. | **[REQ-VAL-01]** | `src/validator.py` |
| **[TASK-BC-03]** | Manejo de Severidades Dinámicas (Context Aware). | **[REQ-VAL-01]** | `src/validator.py` |

### [Ciclo 3] Orquestación e Integración (Día 2 - AM)
| ID Tarea | Tarea Técnica | Tag Trazabilidad | Entregable |
| :--- | :--- | :--- | :--- |
| **[TASK-ARC-01]** | Setup de `main.py` con `argparse` (`--phase`, `--mode`). | **[REQ-ARC-15]** | `main.py` |
| **[TASK-TRACK-01]** | Implementar escritura en `sys_pipeline_execution`. | **[REQ-OUT-03]** | `src/tracker.py` |
| **[TASK-TRACK-02]** | Generación de reporte JSON granular. | **[REQ-OUT-02]** | `src/tracker.py` |

### [Ciclo 4] QA y Estabilización (Día 2 - PM)
| ID Tarea | Tarea Técnica | Tag Trazabilidad | Entregable |
| :--- | :--- | :--- | :--- |
| **[TASK-QA-01]** | Smoke Test: Ejecución completa modo `LOAD` fase `MVP`. | **[MET-04]** | Output Console |
| **[TASK-QA-02]** | Test de Aborto: Simular fallo crítico y validar `exit 1`. | **[ARC-14]** | Audit Log |
| **[TASK-QA-03]** | Test de Feature Flags: Verificar omisión de fuentes desactivadas. | **[REQ-SELECT-01]** | Audit Log |

---

## 5. PLAN DE PRUEBAS Y UAT (Aceptación de Usuario) [IMPL-05]
| Escenario de Prueba | Resultado Esperado | Criterio de Aceptación |
| :--- | :--- | :--- |
| **Contrato Alterado** | Bloqueo por Hash MD5. | El proceso no inicia y reporta `FAIL-SECURITY`. |
| **Datos sin Novedad** | Detección de `NO_NEW_DATA`. | El pipeline termina rápido con estatus `SKIPPED`. |
| **Fallo en Regla Crítica** | Estatus `FAILED` en Supabase. | `main.py` retorna código de error 1. |
| **Advertencia No Crítica**| Estatus `WARNING` en Supabase. | El pipeline continúa pero registra el ruido. |

---

## 6. RITOS DE GOBERNANZA Y CIERRE [IMPL-06]
1.  **Revisión de Trazabilidad**: Verificación de que cada error en el log apunte a un `contract_id` válido.
2.  **Sincronización DVC**: Asegurar que el puntero `.dvc` del contrato esté actualizado tras la validación.
3.  **Aprobación del Gate**: El Stage 2.1 se considera cerrado solo cuando la tabla `sys_pipeline_execution` muestra el primer `SUCCESS` real.

---
## 7. DEFINICIÓN DE TERMINADO (DoD)
*   [x] `main.py` soporta comando `python main.py --phase MVP --mode LOAD`.
*   [x] El reporte JSON se genera en `outputs/reports/phase_MVP/`.
*   [x] Las marcas de agua (`watermark_end`) se actualizan correctamente tras una validación exitosa.
*   [x] El sistema ignora correctamente las fuentes marcadas con `enabled: false`.
*   [x] La trazabilidad con el PRD y SPEC es total (validado mediante este documento).

---
> [!IMPORTANT]
> **Bloqueo Operativo**: La Etapa 2.2 depende de la columna `validation_status` de este stage. Si la validación falla, la carga a producción está prohibida.
