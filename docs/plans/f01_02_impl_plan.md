# Plan de Implementación: Conexión Universal a Base de Datos (Stage 1.2)

## 1. RESUMEN DEL CRONOGRAMA Y EQUIPO (Timeline & Resources)
- **Duración Estimada:** 1 Sprint (1 semana, dado el alcance de infraestructura de conexión).
- **Roles Requeridos:**
    - **Data Engineer (100%):** Implementación del conector y lógica de Singleton.
    - **QA Analyst (50%):** Diseño y ejecución de Unit & Integration Tests.
    - **Product Owner (25%):** Validación de trazabilidad con el Charter.

## 2. RUTA CRÍTICA Y DEPENDENCIAS (Critical Path)
- **Bloqueador Principal:** La visibilidad y permisos de las tablas core en Supabase **[DAT-01]** a **[DAT-06]**.
- **Dependencia:** La implementación del "Data Contract" (Stage 1.3) no puede iniciar hasta que la conexión universal sea declarada estable y segura.
- **Acción Paralela:** El QA puede empezar a escribir los Mocks de las tablas mientras el Data Engineer configura el cliente de Supabase.

## 3. PRODUCT BACKLOG Y WBS (Work Breakdown Structure)

### Épica: Gobernanza de Datos e Infraestructura [EP-01]
| ID | Tarea | Descripción | Responsable | Etiqueta |
| :--- | :--- | :--- | :--- | :--- |
| **T-1.2-01** | Setup del Entorno Seguro | Configuración de `.env` y validación de `.gitignore`. | Data Engineer | **[REQ-SEC-01]** |
| **T-1.2-02** | Core: Singleton Connector | Desarrollo de `DBConnector` con patron Singleton. | Data Engineer | **[REQ-CON-01]** |
| **T-1.2-03** | Proxy de Autenticación | Implementación del Dual-Client (Standard/Service). | Data Engineer | **[REQ-ARC-01]** |
| **T-1.2-04** | Spike: Latencia Supabase | Investigación y medición de tiempos de respuesta. | Data Engineer | **[MET-INF-01]** |
| **T-1.2-05** | Suite de Pruebas Core | Implementación de tests unitarios y de integración. | QA | **[REQ-VAL-01]** |

## 4. PLANIFICACIÓN POR SPRINTS (Sprint Roadmap)

### Sprint 1: Conectividad y Blindaje (Current)
- **Objetivo del Sprint:** Lograr una conexión 100% estable, segura e invisible para el resto de la aplicación, con reporte de calidad generado.
- **Entregables:**
    - `src/connector/db_connector.py` operativo.
    - `tests/reports/tests_report.json` con 100% de éxito.
    - Acceso verificado a los datos diarios **[DAT-01]**.

## 5. PLAN DE PRUEBAS Y UAT (Quality Assurance)
- **Pruebas Técnicas:**
    - **Unitarias:** Validar que `DBConnector()` retorne siempre la misma instancia.
    - **Seguridad:** Confirmar que el uso del `Service Role` sea auditado y lanza excepción si la llave falta.
    - **Integración:** Ejecución de `test_connection()` contra la tabla real de ventas.
- **UAT (Aceptación de Negocio):**
    - Demostración de lectura exitosa de 1 registro de ventas sin exposición de credenciales en pantalla.

## 6. RITOS ÁGILES Y GOBERNANZA
- **Dailies:** 15 min para revisión de impedimentos técnicos en el handshake.
- **Sprint Review:** Presentación del reporte oficial de tests generado automáticamente.
- **Definition of Done (DoD) de la Fase:**
    - Código en `src/` modular y documentado.
    - Pruebas en `tests/` verdes.
    - Reporte consolidado con doble persistencia (Latest/Archive).
    - Trazabilidad total de métricas **[MET-INF-01]** y **[MET-INF-02]** verificada.
