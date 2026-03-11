# Especificaciones Técnicas: Conexión Universal a Base de Datos (Stage 1.2)

## 1. ARQUITECTURA DEL SISTEMA Y DIAGRAMA LÓGICO
- **Arquitectura:** Se adopta un enfoque modular basado en el patrón **Singleton** para la gestión de la persistencia de datos sobre una infraestructura en la nube de **Supabase (PostgreSQL)**. 
- **Flujo de Solución:**
    1.  **Carga de Contexto:** El sistema lee las variables del entorno (`.env`) al arranque.
    2.  **Singleton Guard:** El conector intercepta cualquier solicitud de instancia. Si ya existe un cliente activo, lo retorna; de lo contrario, inicializa la conexión.
    3.  **Encapsulamiento de Clientes:** Se encapsulan dos clientes `supabase-py`: uno estándar (Anon) y uno administrativo (Service Role).
    4.  **Consumo:** Los módulos de extracción (`Stage 1.3+`) invocan el método `get_client()` para interactuar con las tablas a través de PostgREST.

---

## 2. ESPECIFICACIONES DE INGENIERÍA DE DATOS (Data Pipeline)
Vinculadas a los orígenes de datos **[DAT-01]** a **[DAT-09]**.

- **Conectores y Periodicidad:** 
    - **Protocolo:** HTTPS vía REST API (PostgREST) proporcionado por Supabase.
    - **Modo:** Batch (para esta fase de carga histórica inicial).
- **Tratamiento de Datos:**
    - El conector debe facilitar la exportación de resultados en formato `JSON` o `Pandas DataFrame`. 
    - **Resiliencia:** Implementación de bloques `try-except` para manejar inconsistencias de red, asegurando el cumplimiento de **[REQ-INF-02]**.

---

## 3. DISEÑO DEL MODELO DE MACHINE LEARNING (Data Science)
*Aunque esta fase es de infraestructura de datos, el diseño técnico sienta las bases para el entrenamiento:*

- **Estrategia de Entrenamiento:** La arquitectura permite la extracción selectiva de datos por granularidad (Diaria, Mensual) para alimentar el motor de `skforecast` en fases posteriores.
- **Función de Pérdida / Métricas Técnicas:** Se habilita la recolección de métricas de latencia de conexión, impactando indirectamente en la eficiencia del entrenamiento futuro **[MET-INF-01]**.

---

## 4. ESPECIFICACIONES DE INTEGRACIÓN (Software Engineering)
Vinculadas a los requerimientos **[REQ-CON-01]**, **[REQ-SEC-01]** y **[REQ-ARC-01]**.

- **Anatomía del Conector (`src/connector/db_connector.py`):**
    - **Clase:** `DBConnector`
    - **Métodos Clave:**
        - `_initialize_clients()`: Inyecta `SUPABASE_URL` y `SUPABASE_KEY`.
        - `get_client()`: Retorna cliente estándar.
        - `get_service_client()`: Retorna cliente con bypass de RLS (corrobora existencia de `SUPABASE_SERVICE_ROLE_KEY`).
        - `test_connection()`: Ejecuta un `SELECT count` sobre la tabla `ventas` **[DAT-01]** para verificar salud.
- **Esquema de Salida:** Las consultas retornarán objetos serializables, optimizados para su transformación a tipos de datos nativos de Python/Pandas.

---

## 5. MLOPS, INFRAESTRUCTURA Y DESPLIEGUE
- **Gobernanza de Secretos:** Los secretos nunca deben tocar el sistema de archivos de producción de forma plana fuera del entorno de ejecución/memoria.
- **CI/CD - Pruebas Automatizadas:** 
    - **Unitarias:** Verificación del patrón Singleton y manejo de ausencias en `.env`.
    - **Integración:** Validación de Handshake real con latencia < 2s **[MET-INF-01]**.
- **Cómputo:** Ligero (CPU/RAM mínima), optimizado para I/O-bound operations.

---

## 6. MATRIZ DE DISEÑO TÉCNICO VS. PRD

| Componente Técnico | Historia de Usuario / REQ | Etiquetas Vinculadas |
| :--- | :--- | :--- |
| Patrón Singleton en `DBConnector` | Centralización de accesos | **[REQ-CON-01]**, **[ARC-07]** |
| Encapsulamiento de `.env` | Gestión de Secretos | **[REQ-SEC-01]**, **[MET-INF-02]** |
| Dual-Client Proxy (Standard/Service) | Soporte Multi-Tenant | **[REQ-ARC-01]**, **[REQ-INF-03]** |
| `test_connection()` Method | Validación de Conectividad | **[REQ-VAL-01]**, **[MET-INF-01]** |
| Integración con `ventas` table | Ingesta de Datos Core | **[DAT-01]** |
