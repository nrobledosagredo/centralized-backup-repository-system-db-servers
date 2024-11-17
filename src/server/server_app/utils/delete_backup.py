from flask import jsonify
import os
import pymysql.cursors

def delete_backup(request, backups_folder):
    # Obtiene el nombre del archivo de respaldo y el propietario de la solicitud
    backup_name = request.json['backup_name']
    owner = request.json['owner']
    
    # Construye la ruta del archivo de respaldo
    backup_path = os.path.join(backups_folder, owner, backup_name)

    # Si el archivo de respaldo existe, se elimina y devuelve una respuesta exitosa
    if os.path.exists(backup_path):
        os.remove(backup_path)

        # Se conecta a la base de datos y elimina la transacción correspondiente
        connection = pymysql.connect(host=os.getenv('DB_HOST'),
                                     user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASSWORD'),
                                     database=os.getenv('DB_NAME'))

        try:
            with connection.cursor() as cursor:
                # Elimina la transacción correspondiente al respaldo
                sql = "DELETE FROM Transactions WHERE client_id = %s AND filename = %s"
                cursor.execute(sql, (owner, backup_name))
            connection.commit()
        finally:
            connection.close()

        return jsonify({"status": "success", "message": "Backup deleted successfully"}), 200
    else:
        # Si el archivo de respaldo no se encuentra, devuelve un error
        return jsonify({"status": "error", "message": "Backup not found"}), 404