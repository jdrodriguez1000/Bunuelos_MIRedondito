import argparse
import sys
import logging
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
    parser.add_argument("--phase", type=str, default=None, help="Fase de ejecución (ej: MVP, stage_2_1)")
    parser.add_argument("--mode", type=str, choices=["LOAD", "TRAIN", "FORECAST"], default="LOAD", help="Modo de operación")
    
    args = parser.parse_args()
    
    logger.info("==================================================")
    logger.info("🚀 Iniciando Pipeline Mi Redondito")
    logger.info(f"   Modo: {args.mode}")
    logger.info("==================================================")
    
    try:
        # 1. Inicializar Validador
        # El validador detectará automáticamente la fase activa si args.phase es None
        validator = ContractValidator(phase=args.phase)
        logger.info(f"📍 Fase Activa Detectada: {validator.phase_name}")
        
        # 2. EJECUCIÓN DEL GATEKEEPER MULTIFUENTE [ARC-12]
        # validator.validate_pipeline() ahora maneja:
        # - Filtrado por 'enabled: true/false'
        # - Carga de datos
        # - Validaciones de Seguridad, Sincronización y Calidad
        # - Reportes locales y en la nube
        success = validator.validate_pipeline(mode=args.mode)
        
        if not success:
            logger.error("🛑 PIPELINE BLOQUEADO: Una o más fuentes críticas no superaron el contrato.")
            sys.exit(1)
            
        logger.info("🟢 GATEKEEPER EXITOSO: Todas las fuentes activas han sido certificadas.")
        
        # 3. CONTINUACIÓN DEL PIPELINE (Placeholder para futuras etapas de Transformación/ML)
        if args.mode == "LOAD":
            logger.info("💾 Fase de Carga/Ingesta Completada.")
        elif args.mode == "TRAIN":
            logger.info("🧠 Iniciando Entrenamiento de Modelos (Próximamente)...")
        
        logger.info("🏁 Ejecución finalizada con éxito.")

    except Exception as e:
        logger.error(f"💥 Error crítico en la ejecución del pipeline: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
