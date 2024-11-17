import os
import requests
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

def send_backup_to_central_api(file_path):
    # Obtiene la URL de la API central y el nombre del cliente
    central_api_url = os.getenv('CENTRAL_API_RECEIVE_BACKUP_URL')
    username = os.getenv('CLIENT_USERNAME')

    # Abre el archivo y envía una solicitud POST con el archivo y el nombre de usuario como datos
    with open(file_path, 'rb') as file:
        response = requests.post(central_api_url, files={'backup_file': file}, data={'username': username})

    # Retorna verdadero si la solicitud fue exitosa, falso en caso contrario
    return response.status_code == 200