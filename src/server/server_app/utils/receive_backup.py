from flask import jsonify
import os
import datetime
import pymysql.cursors

def receive_backup(request, backups_folder, username, connection):
    # Verifica si se proporcionó un archivo de respaldo en la solicitud
    if 'backup_file' not in request.files:
        return jsonify({"error": "No backup file provided"}), 400

    # Crea una carpeta para los respaldos del usuario si no existe
    user_backups_folder = os.path.join(backups_folder, username)
    if not os.path.exists(user_backups_folder):
        os.makedirs(user_backups_folder)

    # Obtiene el archivo de respaldo de la solicitud
    backup_file = request.files['backup_file']
    backup_filename = backup_file.filename
    
    # Define la ruta donde se guardará el archivo de respaldo
    backup_path = os.path.join(user_backups_folder, backup_filename)

    # Guarda el archivo de respaldo en la carpeta del usuario
    backup_file.save(backup_path)

    # Calcula el tamaño del archivo de respaldo
    backup_size = os.path.getsize(backup_path)

    # Registro del tiempo de finalización del traspaso en la base de datos
    transfer_completion_time = datetime.datetime.now()

    with connection.cursor() as cursor:
        sql = "UPDATE Transactions SET transfer_completion_time = %s, status = 'Completado', size = %s WHERE client_id = %s AND filename = %s"
        cursor.execute(sql, (transfer_completion_time, backup_size, username, backup_filename))
        connection.commit()

    # Retorna un mensaje de éxito en formato JSON
    return jsonify({"status": "success", "message": "Backup file received and saved"}), 200
