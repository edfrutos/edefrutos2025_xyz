from flask import Flask, render_template, redirect, url_for, request
import logging
import sys
import os
from datetime import datetime

# Crear directorio de logs si no existe
log_dir = '/var/www/vhosts/edefrutos2025.xyz/httpdocs/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurar logging
logging.basicConfig(
    filename=os.path.join(log_dir, 'flask_app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/')
def home():
    app.logger.info("Página principal visitada")
    return render_template('home.html')

@app.route('/info')
def info():
    app.logger.info("Página de información visitada")
    server_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('info.html', 
                         python_version=sys.version,
                         current_dir=os.getcwd(),
                         server_time=server_time)

if __name__ == '__main__':
    app.run(debug=True)
