# REGLAS DE NEGOCIO - MI REDONDITO (BUSINESS_RULES)

## 1. Identificación y Control (Metadata)

*   **Título del Documento:** REGLAS DE NEGOCIO (Business Rules)
*   **Versión:** v1.0.0
*   **Estado:** Oficial / Aprobado
*   **Fecha de Creación:** 2026-03-11
*   **Trazabilidad:** Derivado del [project_charter.md](../../docs/artifacts/project_charter.md).
*   **Objetivo:** Formalizar la lógica operativa, comercial y de inventario de **Buñuelos SAS**, sirviendo como base única para la ingeniería de características (Feature Engineering) y las simulaciones del modelo de ML para el proyecto **Mi Redondito**.

---

## 2. Reglas de Producción e Inventario (Operaciones)

### 2.1 Unidad de Medida y Conversión (Kit a Producto)
*   **RN_OPER_001 (Factor de Conversión):** La materia prima se gestiona en "Kits". 1 libra (lb) de Kit equivale exactamente a la producción de **50 buñuelos** de tamaño estándar.
*   **RN_OPER_002 (Integridad del Kit):** El stock en bodega de kits es acumulable y no se pierde. No hay merma de materia prima en bodega para efectos del modelo.

### 2.2 Gestión de Ciclos de Reabastecimiento
La logística de materia prima sigue dos ciclos quincenales:
*   **RN_OPER_003 (Ciclo 1):** Pedido el día 15 de cada mes. Entrega el último día del mes anterior para cubrir la operación del día 1 al 14 del mes siguiente.
*   **RN_OPER_004 (Ciclo 2):** Pedido el día 1 de cada mes. Entrega el día 14 para cubrir la operación desde el día 15 hasta el final del mes.

### 2.3 Dinámica de Producto Terminado (Buñuelo Frito)
*   **RN_OPER_005 (Vida Útil):** Los buñuelos ya preparados (fritos) tienen una vida útil de **un solo día**.
*   **RN_OPER_006 (Merma / Desperdicio):** Cualquier buñuelo frito no vendido al cierre de la jornada se pierde totalmente. El modelo debe minimizar este desperdicio.
*   **RN_OPER_007 (Agotados / Venta Perdida):** Se produce cuando la demanda supera la fritura diaria decidida por el dueño. Estas unidades no atendidas deben ser estimadas para corregir el sesgo de demanda.

---

## 3. Reglas de Estacionalidad y Calendario (Demanda)

### 3.1 Patrones Semanales
*   **RN_DEM_001 (Jerarquía Semanal):** El orden de ventas es Domingo (máximo), seguido de Sábado y luego Viernes.
*   **RN_DEM_002 (Festivos):** Los días festivos se comportan en ventas como si fueran un **Domingo** (Demanda Máxima).

### 3.2 Hitos Mensuales y Pagos
*   **RN_DEM_003 (Días de Quincena):** Las ventas aumentan los días 15, 16, 30 y 31 de cada mes (días de pago en Colombia).
*   **RN_DEM_004 (Prima Legal):** Incremento de ventas del 15 al 20 de junio y del 15 al 20 de diciembre.

### 3.3 Temporadas y Festividades Especiales
*   **RN_DEM_005 (Niveles de Domingo):** Las ventas suben a niveles de un domingo durante:
    *   Novenas Navideñas (16 al 26 de diciembre).
    *   Semana Santa (Jueves y Viernes Santo).
    *   Feria de las Flores (1 al 10 de agosto).
*   **RN_DEM_006 (Meses Top):** Diciembre es el mejor mes, seguido de Enero, Junio y Julio.

---

## 4. Reglas Comerciales y de Marketing

### 4.1 Promociones 2x1
*   **RN_COM_001 (Temporadas 2x1):** Se realizan dos veces al año: del 1 de abril al 31 de mayo, y del 1 de septiembre al 31 de octubre.
*   **RN_COM_002 (Inversión en Ads):** La pauta en Instagram/Facebook inicia 20 días antes de la promoción y se apaga el día 25 del mes final de la misma. El modelo debe capturar este efecto de anticipación.

---

## 5. Factores Externos (Contexto)

### 5.1 Factor Climático
*   **RN_CONT_001 (Efecto Lluvia):** 
    *   Lluvia ligera: Aumenta las ventas (antojo de producto caliente).
    *   Lluvia fuerte/dura: Disminuye las ventas (limita el flujo de personas).

### 5.2 Macroeconomía
*   **RN_CONT_002 (Variables Influyentes):** Salario Mínimo (SMLV), TRM, IPC y tasa de desempleo. El modelo debe evaluar su correlación histórica aunque no haya sido cuantificada previamente por el cliente.

---

## 6. Reglas de Tratamiento de Datos (Atypical)

*   **RN_DATA_001 (Periodo COVID-19):** Los datos del **1 de mayo de 2020 al 30 de abril de 2021** se consideran atípicos (ventas muy bajas por restricciones). Desde mayo 2021 inicia la recuperación y desde 2023 se consideran niveles normales.

---

## 7. Glosario de Términos de Negocio
*   **Kit:** Mezcla de insumos (harina, queso, huevos, etc.) para la producción de buñuelos.
*   **Merma:** Buñuelos ya fritos que no se vendieron el mismo día y son descartados.
*   **Agotado:** Clientes que no pudieron comprar por falta de inventario de producto frito en el momento.
*   **Prima:** Pago legal extraordinario en Colombia (junio y diciembre) que aumenta la capacidad de consumo.
