-- ##############################################################################
-- PROJECT: Bunuelos_MIRedondito
-- STAGE: 1.3 - Data Contract Creation
-- SCRIPT: Create sys_data_contract table and RLS Policies
-- ##############################################################################

-- 1. CREACIÓN DE LA TABLA
CREATE TABLE IF NOT EXISTS public.sys_data_contract (
    id SERIAL PRIMARY KEY,
    contract_id UUID NOT NULL DEFAULT gen_random_uuid(),
    data_contract_payload JSONB NOT NULL,
    statistic_contract_payload JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Comentarios de documentación técnica
COMMENT ON TABLE public.sys_data_contract IS 'Tabla maestra para la persistencia y control de versiones del contrato de datos. Punto de verdad para validaciones en el MVP.';
COMMENT ON COLUMN public.sys_data_contract.contract_id IS 'Identificador único de ejecución del builder.';
COMMENT ON COLUMN public.sys_data_contract.is_active IS 'Flag que indica si este es el contrato vigente para el sistema.';

-- 2. HABILITAR SEGURIDAD DE FILAS (RLS)
ALTER TABLE public.sys_data_contract ENABLE ROW LEVEL SECURITY;

-- 3. POLÍTICAS DE SEGURIDAD [REQ-PER-01]

-- Política de Lectura: Todos los usuarios autenticados pueden leer el contrato activo
CREATE POLICY "Permitir lectura para usuarios autenticados" 
ON public.sys_data_contract 
FOR SELECT 
TO authenticated 
USING (true);

-- Política de Escritura: Solo el service_role (usado por el builder) puede insertar o actualizar
-- Nota: En Supabase, el service_role hace bypass de RLS por defecto, 
-- pero definimos políticas restrictivas para mayor seguridad.
CREATE POLICY "Restringir inserción al service_role" 
ON public.sys_data_contract 
FOR INSERT 
TO service_role 
WITH CHECK (true);

CREATE POLICY "Restringir actualización al service_role" 
ON public.sys_data_contract 
FOR UPDATE 
TO service_role 
USING (true) 
WITH CHECK (true);
