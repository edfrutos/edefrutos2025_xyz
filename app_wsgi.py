import os
import sys
import logging
import traceback  # Añadiendo la importación de traceback

# Configurar logging
logging.basicConfig(
    filename='/var/www/vhosts/edefrutos2025.xyz/httpdocs/flask_app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Añadir el directorio al path
    sys.path.insert(0, '/var/www/vhosts/edefrutos2025.xyz/httpdocs')

    # Activar el entorno virtual si existe
    activate_this = '/var/www/vhosts/edefrutos2025.xyz/httpdocs/.venv/bin/activate_this.py'
    if os.path.exists(activate_this):
        with open(activate_this) as file_:
            exec(file_.read(), dict(__file__=activate_this))
        logger.info("Entorno virtual activado correctamente")
    
    # Importar la aplicación Flask
    from app import app as application
    logger.info("Aplicación Flask importada correctamente")

except Exception as e:
    logger.error(f"Error al inicializar la aplicación: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise