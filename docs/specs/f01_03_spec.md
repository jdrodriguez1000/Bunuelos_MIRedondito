# SPEC: Creación de Contrato de Datos (Stage 1.3)

## 1. ARQUITECTURA DEL SISTEMA Y DIAGRAMA LÓGICO

La arquitectura de la Etapa 1.3 se diseña como un **Service Utility** desacoplado del pipeline productivo, enfocado en la gobernanza y autorregulación del sistema de datos.

### Componentes de Arquitectura [ARC-XX]:
*   **[ARC-09] Configuration Engine**: Módulo basado en `PyYAML` para la ingesta de reglas de negocio desde `config.yaml`.
*   **[ARC-10] Builder Core (In-Memory Processing)**: Motor desarrollado en Python 3.12 que utiliza `pandas` y `numpy` para el perfilamiento estadístico sin persistencia intermedia de datos.
*   **[ARC-11] Hybrid Persistence Layer**: Sistema de triple escritura (Dual Local + Cloud Supabase) para garantizar la alta disponibilidad del contrato.

### Flujo Lógico de la Solución:
1.  **Ingesta de Parámetros**: El `ConfigLoader` valida la estructura de `config.yaml`.
2.  **Conectividad Segura**: Uso del `DBConnector` (Singleton) para abrir el canal con Supabase.
3.  **Reflexión de Esquema**: Ejecución de queries a `information_schema.columns` para validar la existencia física de las fuentes **[DAT-01]** a **[DAT-09]**.
4.  **Perfilamiento Volátil**: Carga de una muestra de datos en memoria para el cálculo de métricas descriptivas y detección de outliers.
5.  **Generación de Artefactos**: Construcción jerárquica de los documentos `data_contract.yaml` y `statistic_contract.json`.
6.  **Sincronización de Estado**: Inserción atómica en Supabase (`sys_data_contract`) e invalidación de contratos previos.

---

## 2. ESPECIFICACIONES DE INGENIERÍA DE DATOS [DAT-XX]

### Pipeline de Introspección (Batch Utility)
*   **Periodicidad**: Ejecución On-Demand (Manual o Trigger de Mantenimiento).
*   **Herramientas**: Python + SQL (Raw Queries para metadatos).

### Feature Engineering & Data Profiling (Technical Specs):
*   **Manejo de Gaps [REG-05]**: Lógica binaria para detectar saltos cronológicos basados en la frecuencia configurada (`D`, `M`, `A`).
*   **Detección de Outliers (Lógica IQR)**:
    *   $Lower\_Bound = Q1 - 1.5 * (Q3 - Q1)$
    *   $Upper\_Bound = Q3 + 1.5 * (Q3 - Q1)$
*   **Análisis Categórico**: Generación de mapas de frecuencia y cálculo de entropía de pesos (Weighting) para detectar desbalances en variables exógenas.

---

## 3. DISEÑO DEL MODELO DE MACHINE LEARNING (Data Science Context)

Aunque esta etapa es de gobernanza, el diseño del contrato está optimizado para la futura integración con `skforecast`:
*   **Estrategia de Validación**: El contrato de datos exige la continuidad temporal mínima requerida para el `ForecasterAutoregDirect` (Lags definidos en fases posteriores).
*   **Validación de Regla de Oro (X-1)**: El contrato incluye metadatos que impiden el uso de datos del día `X` durante el entrenamiento, blindando el sistema contra el **Data Leakage**.

---

## 4. ESPECIFICACIONES DE INTEGRACIÓN Y API [REQ-XX]

### Esquema de Tabla de Salida (Supabase: `sys_data_contract`)
Esta tabla es el punto de integración para el MVP:
| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | SERIAL (PK) | ID interno de base de datos. |
| `contract_id` | UUID | Identificador único de la ejecución (**[REQ-REP-01]**). |
| `data_contract_payload` | JSONB | Estructura YAML convertida a JSON (Reglas). |
| `statistic_contract_payload` | JSONB | Perfil estadístico completo (Soporte). |
| `is_active` | BOOLEAN | Flag de vigencia (**[REQ-INV-01]**). |
| `created_at` | TIMESTAMPTZ | Fecha de creación del contrato. |

### Payloads de Reportabilidad (`builder_report.json`):
```json
{
  "execution_id": "UUID",
  "timestamp": "ISO-8601",
  "status": "SUCCESS/FAILED",
  "metrics": {
    "latency_ms": "int",
    "tables_verified": "int",
    "tables_list": {"table_name": "FOUND/NOT_FOUND"}
  }
}
```

---

## 5. MLOPS, INFRAESTRUCTURA Y DESPLIEGUE

*   **Infraestructura**: Entorno Python local para ejecución; Supabase para orquestación de estado.
*   **Tracking de Experimentos**: El `execution_id` actúa como el puntero de trazabilidad entre la configuración del contrato y los futuros modelos de la Fase 2.
*   **CI/CD**: Las actualizaciones en `config.yaml` deben pasar por un linter de YAML antes de permitir la ejecución del `builder.py`.

---

## 6. MATRIZ DE DISEÑO TÉCNICO VS. PRD

| Componente Técnico | Requerimiento PRD | Etiqueta Trazabilidad |
| :--- | :--- | :--- |
| **ConfigLoader Class** | Orquestación por Configuración | **[REQ-CFG-01]** |
| **Information Schema Query** | Introspección Dinámica | **[REQ-INT-01]** |
| **StatsEngine (Pandas/NumPy)** | Profiling Estadístico | **[REQ-STA-01]** |
| **PersistenceManager** | Persistencia Triple | **[REQ-PER-01]** |
| **Update/Invalidate Logic** | Invalidez Atómica | **[REQ-INV-01]** |
| **JSON Reporter** | Reporte de Ejecución | **[REQ-REP-01]** |

---
> [!NOTE]
> Este documento técnico es la guía definitiva para la implementación de `src/builder.py`. Cualquier desviación del diseño aquí planteado debe ser aprobada mediante el workflow de Control de Cambios.
