import os
import sys
import logging
import traceback

# Configuración de registro
logging.basicConfig(
    filename='/var/www/vhosts/edefrutos2025.xyz/httpdocs/passenger_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Registrar inicio del script
logging.info("Iniciando passenger_wsgi.py")

# Añadir el directorio actual al path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

# Intentar activar entorno virtual si existe
try:
    logging.info("Buscando entorno virtual...")
    venv_path = os.path.join(CURRENT_DIR, '.venv')
    activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
    
    if os.path.exists(activate_this):
        logging.info(f"Activando entorno virtual: {activate_this}")
        with open(activate_this) as file_:
            exec(file_.read(), dict(__file__=activate_this))
        logging.info("Entorno virtual activado correctamente")
    else:
        logging.warning(f"No se encontró el entorno virtual en {venv_path}")
except Exception as e:
    logging.error(f"Error activando entorno virtual: {str(e)}")
    logging.error(traceback.format_exc())

# Importar la aplicación principal con manejo de errores
try:
    logging.info("Intentando importar la aplicación app.py")
    from app import app as application
    logging.info("Aplicación app.py importada correctamente")
except Exception as e:
    logging.error(f"Error importando app.py: {str(e)}")
    logging.error(traceback.format_exc())
    
    # Si la importación falla, usar test.py como fallback
    try:
        logging.info("Intentando importar la aplicación test.py como fallback")
        from test import app as application
        logging.info("Aplicación test.py importada correctamente")
    except Exception as e:
        logging.error(f"Error importando test.py: {str(e)}")
        logging.error(traceback.format_exc())
        
        # Si ambas importaciones fallan, crear una aplicación mínima
        logging.info("Creando aplicación de respaldo")
        from flask import Flask
        
        application = Flask(__name__)
        
        @application.route('/')
        def error_page():
            error_msg = "Error al cargar aplicaciones Flask. Ver los logs para más detalles."
            return error_msg