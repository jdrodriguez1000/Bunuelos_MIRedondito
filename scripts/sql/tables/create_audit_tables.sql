-- ##############################################################################
-- PROJECT: Bunuelos_MIRedondito
-- STAGE: 2.1 - Data Contract Validation
-- DESCRIPTION: Creación de tablas de auditoría y semaforización del pipeline.
-- ##############################################################################

-- 1. TABLA: sys_validation_contract [REQ-OUT-02]
-- Almacena los resultados detallados y granulares de cada validación por tabla.
CREATE TABLE IF NOT EXISTS public.sys_validation_contract (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id_ref INTEGER NOT NULL REFERENCES public.sys_data_contract(id), -- Corregido a INTEGER
    table_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('SUCCESS', 'WARNING', 'FAILED')),
    error_details JSONB, -- Detalles granulares de los fallos encontrados
    validation_timestamp TIMESTAMPTZ DEFAULT now(),
    latency_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. TABLA: sys_pipeline_execution [REQ-OUT-03]
-- Actúa como el Gatekeeper global (Semáforo) para el flujo del pipeline.
CREATE TABLE IF NOT EXISTS public.sys_pipeline_execution (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phase TEXT NOT NULL, -- MVP, CALENDAR, etc.
    mode TEXT NOT NULL, -- LOAD, TRAIN, FORECAST
    contract_id INTEGER NOT NULL REFERENCES public.sys_data_contract(id), -- Corregido a INTEGER
    validation_status TEXT NOT NULL CHECK (validation_status IN ('SUCCESS', 'WARNING', 'FAILED')),
    execution_status TEXT NOT NULL CHECK (execution_status IN ('IN_PROGRESS', 'COMPLETED', 'ABORTED', 'SKIPPED')),
    last_step_completed TEXT, -- VALIDATE, LOAD, etc.
    error_summary TEXT,
    watermark_start TIMESTAMPTZ, -- Puntero de inicio de la validación
    watermark_end TIMESTAMPTZ,   -- Puntero final validado (Nuevo X-1)
    validation_type TEXT CHECK (validation_type IN ('FULL', 'INCREMENTAL', 'NO_NEW_DATA')),
    metadata JSONB, -- Datos adicionales de telemetría
    start_at TIMESTAMPTZ DEFAULT now(),
    end_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. SEGURIDAD: Row Level Security (RLS) e Inactivación de Políticas Inseguras
ALTER TABLE public.sys_validation_contract ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sys_pipeline_execution ENABLE ROW LEVEL SECURITY;

-- Limpieza de políticas antiguas para evitar duplicados o persistencia de avisos
DROP POLICY IF EXISTS "Allow authenticated full access to sys_validation_contract" ON public.sys_validation_contract;
DROP POLICY IF EXISTS "Enable read access for authenticated users" ON public.sys_validation_contract;
DROP POLICY IF EXISTS "Enable insert access for authenticated users" ON public.sys_validation_contract;

DROP POLICY IF EXISTS "Allow authenticated full access to sys_pipeline_execution" ON public.sys_pipeline_execution;
DROP POLICY IF EXISTS "Enable read access for authenticated users" ON public.sys_pipeline_execution;
DROP POLICY IF EXISTS "Enable insert access for authenticated users" ON public.sys_pipeline_execution;
DROP POLICY IF EXISTS "Enable update access for authenticated users" ON public.sys_pipeline_execution;

-- Políticas robustas para sys_validation_contract
CREATE POLICY "sys_val_select_authenticated" 
ON public.sys_validation_contract FOR SELECT 
TO authenticated 
USING ( (select auth.role() = 'authenticated') );

CREATE POLICY "sys_val_insert_authenticated" 
ON public.sys_validation_contract FOR INSERT 
TO authenticated 
WITH CHECK ( (select auth.role() = 'authenticated') );

-- Políticas robustas para sys_pipeline_execution
CREATE POLICY "sys_pipe_select_authenticated" 
ON public.sys_pipeline_execution FOR SELECT 
TO authenticated 
USING ( (select auth.role() = 'authenticated') );

CREATE POLICY "sys_pipe_insert_authenticated" 
ON public.sys_pipeline_execution FOR INSERT 
TO authenticated 
WITH CHECK ( (select auth.role() = 'authenticated') );

CREATE POLICY "sys_pipe_update_authenticated" 
ON public.sys_pipeline_execution FOR UPDATE 
TO authenticated 
USING ( (select auth.role() = 'authenticated') )
WITH CHECK ( (select auth.role() = 'authenticated') );

-- 4. COMENTARIOS DE TABLA (Metadatos Cloud)
COMMENT ON TABLE public.sys_validation_contract IS 'Auditoría detallada de validaciones de contrato de datos.';
COMMENT ON TABLE public.sys_pipeline_execution IS 'Semáforo de control y estado de ejecución del pipeline Mi Redondito.';
