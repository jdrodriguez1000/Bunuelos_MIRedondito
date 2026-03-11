# Project Plan: Bunuelos_MIRedondito

## Executive Summary
This document outlines the execution roadmap for the demand forecasting system of **Bunuelos SAS**. Following the philosophies **"Less is More"**, **"Production First"**, and **"Spec-Driven Development (SDD)"**, we ensure that every development stage is preceded by robust documentation (REQ, SPEC, IMPL). This guarantees automation through Python modules (`src/`) and a MAPE < 15% using `skforecast`.

---

## 📈 Phase Execution Status

| Phase | Description | Status | Start Date | End Date |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Kickoff and Implementation** | **IN PROGRESS** | 2026-03-11 | TBD |
| **02** | **Minimum Viable Product (MVP) - Endogenous Variables** | Pending | - | - |
| **03** | **Robustness - Calendar** | Pending | - | - |
| **04** | **Controllable Variables - Commercial & Marketing** | Pending | - | - |
| **05** | **External Non-Controllable Variables - Macro & Weather** | Pending | - | - |
| **06** | **"Black Swan" Events** | Pending | - | - |
| **07** | **Simulation & "What-If" Scenarios** | Pending | - | - |

---

## 🏗️ Detailed Phase 01: Kickoff and Implementation
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

---

## 🎯 Milestones
1. **M1 (Infra Ready):** All directories and base docs established.
2. **M2 (Connection Established):** Successful data pull from Supabase with logs.
3. **M3 (Data Contract Signed):** Schemas validated and frozen for MVP.

---
*Last Edited: 2026-03-11*
