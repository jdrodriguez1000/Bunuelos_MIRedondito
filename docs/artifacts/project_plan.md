# Project Plan: Bunuelos_MIRedondito

## Executive Summary
This document outlines the execution roadmap for the demand forecasting system of **Bunuelos SAS**. Following the philosophies **"Less is More"**, **"Production First"**, and **"Spec-Driven Development (SDD)"**, we ensure that every development stage is preceded by robust documentation (REQ, SPEC, IMPL). This guarantees automation through Python modules (`src/`) and a MAPE < 15% using `skforecast`.

---

## 📈 Phase Execution Status

| Phase | Description | Status | Start Date | End Date |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Kickoff and Implementation** | **COMPLETED** | 2026-03-11 | 2026-03-11 |
| **02** | **Minimum Viable Product (MVP) - Endogenous Variables** | **IN PROGRESS** | 2026-03-11 | TBD |
| **03** | **Robustness - Calendar** | Pending | - | - |
| **04** | **Controllable Variables - Commercial & Marketing** | Pending | - | - |
| **05** | **External Non-Controllable Variables - Macro & Weather** | Pending | - | - |
| **06** | **"Black Swan" Events** | Pending | - | - |
| **07** | **Simulation & "What-If" Scenarios** | Pending | - | - |

---

## 🏗️ Detailed Phase 01: Kickoff and Implementation (COMPLETED)
**Objective:** Establish the project's technical skeleton, environment setup, and secure the data bridge with Supabase.

### Stage 1.1: Infrastructure and Documentation (COMPLETED)
- [x] Formalization of SDD: [REQ](../reqs/f01_01_requirements.md), [SPEC](../specs/f01_01_spec.md), [IMPL](../plans/f01_01_impl_plan.md).
- [x] Creation of the Project Charter.
- [x] Definition of Project Rules (`.clinerules`).
- [x] Creation of the Global Rules (`global_rules.md`).
- [x] Creation of the Business Rules (`business_rules.md`).
- [x] Creation of the Technical Rules (`technical_rules.md`).
- [x] Creation of the Strategic Rules (`strategic_rules.md`).
- [x] Setup of the Master Index (`index.md`).
- [x] Creation of the Project Plan.
- [x] Creation of GitHub Governance (`github_rules.md`, `SKILL.md`, `workflow`).
- [x] Initialization of DVC (Data Version Control) and Remote Storage.
- [x] Setup of Virtual Environment (Python 3.12+).
- [x] Creation of `requirements.txt` and dependency installation.
- [x] Setup of Strategic Communication Governance (Rules, Skill, Workflow).
- [x] Setup of Change Control Governance (Rules, Skill, Workflow).
- [x] Setup of Lessons Learned Governance (Rules, Skill, Workflow).
- [x] Setup of Quality Assurance Governance (Rules, Skill, Workflow).
- [x] Creation of Testing Structure (`tests/unit`, `tests/integration`, `tests/functional`, `tests/reports`).

### Stage 1.2: Database Connection (COMPLETED)
- [x] Refinamiento de Documentación SDD a Nivel Senior: [PRD](../reqs/f01_02_requirements.md), [SPEC](../specs/f01_02_spec.md), [IMPL Plan](../plans/f01_02_impl_plan.md).
- [x] Configuración de variables de entorno segura (`.env`) y blindaje de secretos.
- [x] Implementación de `DBConnector` bajo patrón **Singleton** y **Dual-Client Proxy**.
- [x] Creación del Framework de Reportabilidad QA (Scripts de consolidación y doble persistencia).
- [x] Ejecución y validación de Pipeline de Calidad (Unit & Integration Tests).
- [x] Prueba de conectividad exitosa y validación de latencia [MET-INF-01].

### Stage 1.3: Data Contract Creation (COMPLETED)
- [x] Refinamiento de Documentación SDD a Nivel Senior: [PRD](../reqs/f01_03_requirements.md), [SPEC](../specs/f01_03_spec.md), [IMPL Plan](../plans/f01_03_impl_plan.md).
- [x] **[EP-01] Infraestructura y Configuración**:
    - [x] Setup de `config.yaml` parametrizado con las 9 fuentes [REQ-CFG-01].
    - [x] Creación de la tabla `sys_data_contract` en Supabase [REQ-PER-01].
- [x] **[EP-02] Motor de Introspección y Perfilamiento**:
    - [x] Desarrollo del `Introspector` dinámico con paginación recursiva para >1000 registros [REQ-INT-01].
    - [x] Implementación del `StatsEngine` y motor de Outliers (IQR) [REQ-STA-01].
- [x] **[EP-03] Persistencia y Reportabilidad**:
    - [x] Implementación del Manager de Triple Persistencia (Dual Local + Cloud) [REQ-PER-01].
    - [x] Generación de Reporte de Ejecución `builder_report.json` [REQ-REP-01].
    - [x] Integración de trazabilidad total mediante `contract_id` y `dvc_hash`.
- [x] **[EP-04] Quality Assurance y Validación**:
    - [x] [QA-01] Validación de consistencia de Hash MD5 entre archivos locales y Supabase.
    - [x] [QA-02] Prueba de carga de volumen para verificar paginación (>1000 registros).
    - [x] [QA-03] Unit tests para el cálculo de métricas (IQR, Mediana).
    - [x] [QA-04] Integration test de persistencia atómica en Supabase (Invalidación + Inserción).
    - [x] [QA-05] Verificación de esquema YAML contra esquemas físicos reales.
- [x] **[EP-05] Gobierno y Documentación**:
    - [x] Institucionalización de Prompts Maestros como Habilidad (`project_lifecycle_expert`).
    - [x] Implementación de Workflow de Gestión de Documentación SDD (`manage_project`).

---

## 🏗️ Detailed Phase 02: Minimum Viable Product (MVP) - Endogenous Variables (IN PROGRESS)
**Objective:** Build a robust forecasting baseline using internal historical sales data and technical demand variables.

> [!IMPORTANT]
> **Exclusiones de esta Fase:**
> 1. **Monitoreo y Control Automático:** No se implementarán triggers de re-entrenamiento ni alertas de drift operativos en esta fase.
> 2. **Simulaciones "What-If":** No se incluirá el motor de escenarios (Precios, Promociones, Clima) en el MVP.

### Stage 2.1: Data Contract Validation (IN PROGRESS)
- [x] Refinamiento de Documentación SDD a Nivel Senior: [PRD](../reqs/f02_01_requirements.md), [SPEC](../specs/f02_01_spec.md), [IMPL Plan](../plans/f02_01_impl_plan.md).
- [ ] **[EP-06] Guardrail de Calidad y Semaforización**:
    - [ ] **Configuración e Infraestructura Cloud**:
        - [ ] Ajuste de `config.yaml` para segmentación por fases (MVP/Futuross) [REQ-CFG-01].
        - [ ] Creación física de la tabla `sys_validation_contract` en Supabase [REQ-OUT-02].
        - [ ] Creación física de la tabla `sys_pipeline_execution` en Supabase [REQ-OUT-03].
    - [ ] **Núcleo de Validación y Seguridad**:
        - [ ] Implementación de `IntegrityChecker` (MD5 local vs Cloud) [REQ-HAS-01].
        - [ ] Desarrollo del `WatermarkManager` (Lógica FULL/INC/SKIP) [REQ-WAT-01].
        - [ ] Componente `ContractValidator` con reglas vectorizadas [REQ-VAL-01].
    - [ ] **Orquestación final**:
        - [ ] Creación de `main.py` como entrypoint CLI (--phase, --mode) [REQ-ARC-15].
    - [ ] **QA y Estabilización**:
        - [ ] Validación de "Regla de Oro" (Fijación de puntero en X-1).
        - [ ] Prueba de estrés de validación con volúmenes de datos reales.
        - [ ] Simulación de aborto por incoherencia de contrato (Smoke Test).

### Stage 2.2: Data Loading (PENDING)
- [ ] Refinamiento de Documentación SDD: [PRD](../reqs/f02_02_requirements.md), [SPEC](../specs/f02_02_spec.md), [IMPL Plan](../plans/f02_02_impl_plan.md).
- [ ] **[EP-07] Ingesta Distribuida de Fuentes**:
    - [ ] Implementación de `DataLoader` modular para las fuentes [DAT-01] a [DAT-06].
    - [ ] Gestión de memoria y paginación para lectura segura de Supabase.

### Stage 2.3: Data Preprocessing (PENDING)
- [ ] Refinamiento de Documentación SDD: [PRD](../reqs/f02_03_requirements.md), [SPEC](../specs/f02_03_spec.md), [IMPL Plan](../plans/f02_03_impl_plan.md).
- [ ] **[EP-08] Armonización y Cálculo de Target**:
    - [ ] Cálculo de `Demanda_Teorica_Total` [REG-06] (Ventas + Agotados).
    - [ ] Sincronización cronológica para asegurar serie continua sin ceros estructurales (Venta diaria garantizada).

### Stage 2.4: Exploratory Data Analysis (EDA) (PENDING)
- [ ] Refinamiento de Documentación SDD: [PRD](../reqs/f02_04_requirements.md), [SPEC](../specs/f02_04_spec.md), [IMPL Plan](../plans/f02_04_impl_plan.md).
- [ ] **[EP-09] Análisis de Señal y Ruido**:
    - [ ] Análisis de Autocorrelación (ACF/PACF) de la demanda.
    - [ ] Identificación de estacionalidad semanal y outliers históricos.

### Stage 2.5: Feature Engineering (PENDING)
- [ ] Refinamiento de Documentación SDD: [PRD](../reqs/f02_05_requirements.md), [SPEC](../specs/f02_05_spec.md), [IMPL Plan](../plans/f02_05_impl_plan.md).
- [ ] **[EP-10] Creación de Características Endógenas**:
    - [ ] Definición de Lags y Ventanas Móviles (Rolling Statistics).
    - [ ] Variables de tiempo básicas (Día_Semana, Fin_Semana).

### Stage 2.6: Training and Modeling (PENDING)
- [ ] Refinamiento de Documentación SDD: [PRD](../reqs/f02_06_requirements.md), [SPEC](../specs/f02_06_spec.md), [IMPL Plan](../plans/f02_06_impl_plan.md).
- [ ] **[EP-11] Entrenamiento y Experimentación**:
    - [ ] Implementación de `ForecasterAutoregDirect` (Benchmarking `Ridge` vs `Trees`).
    - [ ] **Experimento A**: Entrenamiento con peso uniforme de la serie histórica.
    - [ ] **Experimento B**: Entrenamiento con decaimiento de peso temporal (Prioridad a data reciente).
    - [ ] Evaluación mediante Backtesting y métricas comparativas (MAPE vs Naive Benchmark).

### Stage 2.7: Invisibility & Inference (PENDING)
- [ ] Refinamiento de Documentación SDD: [PRD](../reqs/f02_07_requirements.md), [SPEC](../specs/f02_07_spec.md), [IMPL Plan](../plans/f02_07_impl_plan.md).
- [ ] **[EP-12] Pronóstico Horizonte 95**:
    - [ ] Generación de predicciones a futuro respetando la Regla X-1.
    - [ ] Post-procesamiento: Recorte de incertidumbre y agregación por meses.

### Stage 2.8: Dashboard Layout & Construction (PENDING)
- [ ] Refinamiento de Documentación SDD: [PRD](../reqs/f02_08_requirements.md), [SPEC](../specs/f02_08_spec.md), [IMPL Plan](../plans/f02_08_impl_plan.md).
- [ ] **[EP-13] Visualización y Storytelling**:
    - [ ] Construcción del Dashboard v1 con visualización de Pronóstico.
    - [ ] Implementación de Módulo de Conversión: `Demanda (Unidades) -> Pedido Sugerido (Libras de Kit)`.
    - [ ] Generación de Reporte Ejecutivo de Fase (Wow Factor).
    - [ ] Documentación de Lecciones Aprendidas del MVP.

---

## 🎯 Hitos (Milestones)
1. **M1 (Infraestructura Lista):** Todos los directorios y documentos base establecidos.
2. **M2 (Conexión Establecida):** Extracción de datos exitosa desde Supabase con logs verificados.
3. **M3 (Contrato de Datos Firmado):** Esquemas validados y congelados para el inicio del MVP.
4. **M4 (Baseline Endógeno):** Primer modelo de pronóstico operativo con métricas de error iniciales.
5. **M5 (MVP Entregado):** Dashboard v1 funcional y reporte ejecutivo de cierre de fase.

---
*Last Edited: 2026-03-11*
