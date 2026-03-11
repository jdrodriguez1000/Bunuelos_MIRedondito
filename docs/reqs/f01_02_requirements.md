# PRD: Conexión Universal a Base de Datos (Stage 1.2)

## 1. RESUMEN Y ALINEACIÓN (Overview & Alignment)

### Propósito específico de esta Fase
Garantizar la **integridad, seguridad y disponibilidad** de los datos históricos de Bunuelos SAS mediante la implementación de una capa de persistencia técnica robusta. El objetivo es eliminar la fragmentación de accesos a datos y establecer un "Single Point of Truth" (SPoT) para el motor de forecasting, permitiendo que el sistema sea agnóstico a cambios futuros en el proveedor de nube (Neutralidad de Datos).

### Tabla de Trazabilidad de la Fase
| Entregable | Objetivos Vinculados [OBJ-XX] | Requerimientos de Alto Nivel [REQ-XX] |
| :--- | :--- | :--- |
| **[DEL-02]** Database Connection | **[OBJ-04]** Automatización Técnica<br>**[OBJ-05]** Neutralidad de Datos | **[REQ-INF-01]** Centralización de Datos en Supabase<br>**[REQ-INF-02]** Acceso Seguro y Encriptado<br>**[REQ-INF-03]** Soporte Multi-Tenant (Standard vs Admin) |

---

## 2. ALCANCE ESPECÍFICO DE LA FASE (Scope)

### Qué está INCLUIDO (In Scope)
*   **[REQ-CON-01] Conector Universal:** Desarrollo de `src/connector/db_connector.py` utilizando el patrón Singleton para optimizar el pool de conexiones.
*   **[REQ-SEC-01] Gestión de Secretos:** Implementación de inyección de dependencias mediante variables de entorno (`.env`) para evitar el hardcoding de credenciales.
*   **[REQ-ARC-01] Dual-Access Client:** Capacidad de instanciar un cliente estándar (RLS activo) para consultas de lectura y un cliente de Rol de Servicio para tareas administrativas.
*   **[REQ-VAL-01] Connectivity Smoke Tests:** Suite de validación automatizada para asegurar latencia aceptable y visibilidad de las 9 tablas core.

### Qué está EXCLUIDO (Out of Scope)
*   Definición de esquemas o migraciones de tablas (corresponde al Stage 1.3).
*   Lógica de limpieza o imputación de nulos.
*   Persistencia de archivos físicos (DVC).

---

## 3. CASOS DE USO Y ÉPICAS (User Stories & Epics)

### Épica: Acceso Seguro y Unificado a Datos [EP-01]
*   **User Story 1:** Como **Data Engineer**, quiero un conector centralizado en `src/` para que no tenga que re-escribir la lógica de autenticación en cada script de extracción vinculado a **[REQ-CON-01]**.
*   **User Story 2:** Como **Analista de Seguridad**, quiero que las llaves de Supabase residan fuera del código fuente para cumplir con los estándares de gobernanza técnica de Triple S vinculado a **[REQ-SEC-01]**.
*   **User Story 3:** Como **Sistema de Forecasting**, quiero validar la conexión antes de iniciar un proceso largo de entrenamiento para fallar rápido en caso de caída del servicio vinculado a **[REQ-VAL-01]**.

---

## 4. REQUERIMIENTOS TÉCNICOS Y DE DATOS (Data Requirements)

### Ingeniería de Datos y Fuentes
*   **Target:** El conector debe ser capaz de acceder a las fuentes diarias **[DAT-01]** a **[DAT-06]**, mensuales **[DAT-07]**-**[DAT-08]** y anuales **[DAT-09]**.
*   **Granularidad:** Soporte para consultas atómicas (filas individuales) y descargas masivas para entrenamiento.
*   **Manejo de Errores:** El conector debe capturar y loguear excepciones de conectividad, distinguiendo entre errores de autenticación (401) y errores de red (Timeout).

---

## 5. INGENIERÍA Y ARQUITECTURA [ARC-XX]

### Diseño del Sistema
*   **[ARC-07] Singleton Interface:** La clase `DBConnector` no debe permitir recrear el cliente innecesariamente, ahorrando recursos de memoria y conexiones abiertas en Supabase.
*   **[ARC-08] Software Stack:** Uso estricto de `supabase-py` (v2.x) y `python-dotenv`.
*   **Latencia:** El "Handshake" inicial no debe exceder los 2 segundos en condiciones normales de red.

---

## 6. CRITERIOS DE ACEPTACIÓN Y MÉTRICAS DE LANZAMIENTO (Release Criteria)

### Definición de Hecho (Definition of Done - DoD)
1.  **Validación de Clase:** `DBConnector` implementado con persistencia de instancia única.
2.  **Seguridad:** Verificación de que el archivo `.env` está en `.gitignore`.
3.  **Cobertura de Pruebas:**
    *   100% de pruebas unitarias (`tests/unit`) exitosas (Singleton, Exception Handling).
    *   Prueba de integración real (`tests/integration`) confirmando lectura de la tabla `ventas`.
4.  **Doble Persistencia:** Reporte de calidad generado en `tests/reports/tests_report.json` y archivado en histórico.

### Métricas Técnicas [MET-XX]
*   **[MET-INF-01] Conectividad:** 100% de éxito en el handshake inicial bajo credenciales válidas.
*   **[MET-INF-02] Aislamiento:** Zero (0) ocurrencias de credenciales planas en los logs de ejecución.

---

> [!IMPORTANT]
> Este documento ha sido reconstruido para alinearse con el **Project Charter v1.0**. Todas las implementaciones futuras en el Stage 1.2 deben referenciar estas etiquetas de trazabilidad.
