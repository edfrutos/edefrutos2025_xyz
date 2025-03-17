# Añadir importaciones necesarias
import os
import traceback
import logging
from functools import wraps
from flask import Flask, jsonify, current_app, request, render_template
from pymongo import MongoClient

# Configurar el logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Función para registrar los errorhandlers en la app Flask
def register_error_handlers(app):
    @app.errorhandler(500)
    def handle_500(e):
        logger.error(f"Error 500: {str(e)}")
        return render_template("error.html", error=str(e)), 500
        
    @app.errorhandler(404)
    def handle_404(e):
        return render_template("not_found.html"), 404

# Función decoradora para manejar excepciones en rutas
def route_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Registrar el error en logs
            error_msg = f"Error en {func.__name__}: {str(e)}"
            stack_trace = traceback.format_exc()
            logger.error(f"{error_msg}\n{stack_trace}")
            
            # Si estamos en una ruta que maneja JSON, devolver JSON
            if request.path.startswith('/api/'):
                return jsonify({"error": str(e)}), 500
            
            # Mostrar una página de error amigable con detalles técnicos
            return render_template("error.html", error=str(e), 
                                 traceback=stack_trace), 500
    
    return wrapper

# Mejorar el manejo de la conexión con MongoDB
def get_db_connection():
    try:
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            logger.error("Variable de entorno MONGO_URI no definida")
            raise ValueError("MONGO_URI environment variable is not set")
            
        client = MongoClient(mongo_uri)
        # Comprobar conexión
        client.admin.command('ismaster')
        
        db = client.catalogo
        logger.info("Conexión a MongoDB establecida correctamente")
        return db
    except Exception as e:
        logger.error(f"Error al conectar con MongoDB: {str(e)}")
        raise

# Función principal para aplicar todos los fixes a una aplicación Flask
def apply_fixes(app):
    register_error_handlers(app)

