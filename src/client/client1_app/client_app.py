# Importa las bibliotecas necesarias
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Importa las funciones en /utils
from utils.database_backup import create_database_backup
from utils.compress import compress_file
from utils.encrypt import encrypt_file, decrypt_file
from utils.send_backup import send_backup_to_central_api
from utils.delete_backup import delete_backup_file
from utils.scheduler import schedule_backup

# Carga las variables de entorno del archivo .env
load_dotenv()

# Obtiene el host y el puerto de la aplicación del archivo .env
app_host = os.getenv('CLIENT_APP_HOST')
app_port = int(os.getenv('CLIENT_APP_PORT'))

# Configura el nombre del archivo de log
log_filename = os.path.join('logs', os.getenv('CLIENT_USERNAME') + '.log')

# Configuración del logging
log_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
log_handler = RotatingFileHandler(log_filename, mode='a', maxBytes=5*1024*1024, backupCount=10, encoding=None, delay=0)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

logger = logging.getLogger('custom_logger')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Crea una instancia de la aplicación Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Ruta para obtener la lista de respaldos en la carpeta /files
@app.route('/api/get_backups', methods=['GET'])
def get_backups():
    files = [f for f in os.listdir('./files') if f.endswith('.enc')]
    return jsonify(files)

# Ruta para realizar la solicitud de desencriptar un respaldo encriptado
@app.route('/api/decrypt_backup', methods=['POST'])
def decrypt_backup():
    # Obtiene el nombre del archivo desde la petición
    filename = request.json.get('filename')

    if filename is None:
        return jsonify({"error": "filename is missing"}), 400

    # Verifica que el archivo exista
    if not os.path.exists(f'./files/{filename}'):
        return jsonify({"error": "file does not exist"}), 404

    # Desencripta el archivo
    decrypted_filepath = decrypt_file(f'./files/{filename}')

    if decrypted_filepath is None:
        return jsonify({"error": "file decryption failed"}), 500

    return jsonify({"message": "file decrypted successfully", "filename": decrypted_filepath})


# Define la función de respaldo
def backup_db():
    # Crea un respaldo de la base de datos
    backup_filepath = create_database_backup()
    logger.info("Database backup created: %s", backup_filepath)
    # Comprime el archivo de respaldo
    compressed_backup_filepath = compress_file(backup_filepath)
    logger.info("Backup file compressed: %s", compressed_backup_filepath)
    # Encripta el archivo de respaldo comprimido
    encrypted_backup_filepath = encrypt_file(compressed_backup_filepath)
    logger.info("Backup file encrypted: %s", encrypted_backup_filepath)

    # Envía el archivo de respaldo encriptado a la API server
    success = send_backup_to_central_api(encrypted_backup_filepath)
    if success:
        logger.info("Backup file sent successfully")
        # Si el archivo de respaldo se envió correctamente, elimina los archivos locales
        delete_backup_file(backup_filepath)
        delete_backup_file(compressed_backup_filepath)
        delete_backup_file(encrypted_backup_filepath)
        logger.info("Local copies deleted")
    else:
        # Si no se pudo enviar el archivo de respaldo, devuelve un error
        logger.error("Failed to send the encrypted backup file to the server API")

# Programa la primera tarea de respaldo
schedule_backup(backup_db)

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, host=app_host, port=app_port)