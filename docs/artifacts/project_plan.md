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
- [x] Setup of Change Control Governance (Rules, Workflow).

### Stage 1.2: Database Connection (CURRENT)
- [ ] Configuration of environment variables (`.env`) and secure credentials.
- [ ] Implementation of the Supabase Connector helper.
- [ ] Connection validation and latency test.

### Stage 1.3: Data Contract Creation
- [ ] Introspection of Supabase tables.
- [ ] Definition of data types, constraints, and valid ranges.
- [ ] Freezing of schemas for the MVP phase.

---

## 🎯 Milestones
1. **M1 (Infra Ready):** All directories and base docs established.
2. **M2 (Connection Established):** Successful data pull from Supabase with logs.
3. **M3 (Data Contract Signed):** Schemas validated and frozen for MVP.

---
*Last Edited: 2026-03-11*
