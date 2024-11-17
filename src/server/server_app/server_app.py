from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql.cursors
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from utils.receive_backup import receive_backup
from utils.delete_backup import delete_backup
from utils.get_backups import get_backups

# Carga las variables de entorno del archivo .env
load_dotenv()

# Obtiene el host y el puerto de la aplicación del archivo .env
app_host = os.getenv('SERVER_APP_HOST')
app_port = int(os.getenv('SERVER_APP_PORT'))

# Obtiene las credenciales de la base de datos del archivo .env
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Configura el nombre del archivo de log
log_filename = os.path.join('logs', 'server.log')

# Configuración del logging
log_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
log_handler = RotatingFileHandler(log_filename, mode='a', maxBytes=5*1024*1024, backupCount=10, encoding=None, delay=0)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

# Usa un nombre de logger personalizado en lugar de 'root'
logger = logging.getLogger('custom_logger')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Crea una instancia de la aplicación Flask y habilita CORS
app = Flask(__name__)
CORS(app)

# Carpeta donde se almacenarán los respaldos recibidos
backups_folder = "central_repository"

# Establece la conexión a la base de datos
connection = pymysql.connect(host=db_host,
                             port=int(db_port),
                             user=db_user,
                             password=db_password,
                             database=db_name,
                             cursorclass=pymysql.cursors.DictCursor)

# Ruta para obtener la lista de todos los respaldos
@app.route('/api/get_backups', methods=['GET'])
def get_all_backups():
    return get_backups(backups_folder)

# Ruta para eliminar un archivo de respaldo específico
@app.route('/api/delete_backup', methods=['POST'])
def delete_backup_file():
    backup_name = request.json.get('backup_name')
    owner = request.json.get('owner')
    logger.info(f"Deleting backup '{backup_name}' for owner '{owner}'")
    return delete_backup(request, backups_folder)

# Ruta para recibir respaldos de los clientes
@app.route('/api/receive_backup', methods=['POST'])
def receive_client_backup():
    username = request.form['username']

    # Registro del tiempo de solicitud en la base de datos
    request_time = datetime.now()

    with connection.cursor() as cursor:
        sql = "INSERT INTO Transactions (client_id, filename, request_time, status, size) VALUES (%s, %s, %s, 'En proceso', 0)"
        cursor.execute(sql, (username, request.files['backup_file'].filename, request_time))
        connection.commit()

    logger.info("Backup received from client: %s", username)  # Registra el evento

    return receive_backup(request, backups_folder, username, connection)

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, host=app_host, port=app_port)