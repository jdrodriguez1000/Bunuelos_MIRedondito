import argparse
import sys
import logging
import pandas as pd
from datetime import datetime
from src.connector.db_connector import DBConnector
from src.validator import ContractValidator

# 1. Configuración de Logging de Alto Nivel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
)
logger = logging.getLogger("Forecaster_Main")

def main():
    """
    Entrypoint principal del sistema Forecaster.
    Orquesta la ejecución del pipeline con enfoque en el Gatekeeper de Datos.
    [REQ-ARC-15]
    """
    parser = argparse.ArgumentParser(description="Forecaster Pipeline Orchestrator")
    parser.add_argument("--phase", type=str, default="validation_mvp", help="Fase de ejecución (ej: validation_mvp)")
    parser.add_argument("--mode", type=str, choices=["LOAD", "TRAIN", "FORECAST"], default="LOAD", help="Modo de operación")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Iniciando Pipeline: Fase={args.phase} | Modo={args.mode}")
    
    try:
        # 1. Conexión a Base de Datos
        db = DBConnector()
        client = db.get_client()
        
        # 2. Inicializar Validador
        validator = ContractValidator(phase=args.phase)
        target_table = validator.target_table
        
        # 3. Carga de Datos (Extracción Inicial para Validación)
        # Nota: En un entorno productivo, esto podría ser incremental basado en watermarks.
        # Por ahora, cargamos una muestra o el total para el MVP.
        logger.info(f"📥 Cargando datos desde tabla: {target_table}")
        
        # Superamos el límite de 1000 de Supabase si es necesario
        all_data = []
        chunk_size = 1000
        start = 0
        while True:
            response = client.table(target_table).select("*").range(start, start + chunk_size - 1).execute()
            all_data.extend(response.data)
            if len(response.data) < chunk_size:
                break
            start += chunk_size
            
        df = pd.DataFrame(all_data)
        
        if df.empty:
            logger.error(f"❌ La tabla {target_table} no retornó datos. Abortando.")
            sys.exit(1)
            
        logger.info(f"✅ Datos cargados correctamente: {len(df)} registros.")

        # 4. EJECUCIÓN DEL GATEKEEPER [SPEC-PIP-01]
        # Este componente orquesta Seguridad, Sincronización y Calidad
        is_valid = validator.validate_gate(df)
        
        if not is_valid:
            logger.error("🛑 PIPELINE BLOQUEADO: Los datos no superaron el contrato de calidad.")
            sys.exit(1)
            
        logger.info("🟢 GATEKEEPER EXITOSO: Procediendo con el resto del pipeline...")
        
        # 5. CONTINUACIÓN DEL PIPELINE (Placeholder para futuras etapas)
        if args.mode == "LOAD":
            logger.info("💾 Modo LOAD: Datos validados y listos para persistencia de staging.")
        elif args.mode == "TRAIN":
            logger.info("🧠 Modo TRAIN: Iniciando entrenamiento de modelos con datos certificados.")
            # Aquí se llamaría al motor de ML
        
        logger.info("🏁 Pipeline finalizado con éxito.")

    except Exception as e:
        logger.error(f"💥 Error crítico en la ejecución del pipeline: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
