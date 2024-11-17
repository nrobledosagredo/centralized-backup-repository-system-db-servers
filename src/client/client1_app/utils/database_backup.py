# Importa las bibliotecas necesarias
import os
import subprocess
from datetime import datetime

def create_database_backup():
    # Obtiene las variables de entorno de la conexión a la base de datos
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')
    db_type = os.getenv('DB_TYPE')

    # Obtiene la marca de tiempo actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Crea una ruta de archivo para el archivo de respaldo, incluyendo la marca de tiempo
    backup_filepath = f"{database}_backup_{timestamp}.sql"

    # Define el comando de respaldo según el tipo de base de datos
    if db_type == "mariadb" or db_type == "mysql":
        backup_command = ["mysqldump", f"--host={host}", f"--user={user}", f"--password={password}", database]
    elif db_type == "postgresql":
        os.environ['PGPASSWORD'] = password
        backup_command = ["pg_dump", f"--host={host}", f"--username={user}", f"--dbname={database}"]

    # Abre el archivo de respaldo y ejecuta el comando de respaldo
    with open(backup_filepath, "wb") as f:
        process = subprocess.Popen(backup_command, stdout=f)
        # Espera a que finalice el proceso de respaldo y obtiene el código de salida
        exit_code = process.wait()

    # Si el código de salida no es 0, se produjo un error y se retorna None
    if exit_code != 0:
        print(f"Error al crear el respaldo de {database}: Código de salida {exit_code}")
        return None

    # Retorna la ruta del archivo de respaldo si se creó correctamente
    return backup_filepath