from flask import jsonify
import os

def get_backups(backups_folder):
    # Si la carpeta de respaldos no existe, se crea
    if not os.path.exists(backups_folder):
        os.makedirs(backups_folder)

    # Obtiene la lista de clientes en la carpeta de respaldos
    clients = os.listdir(backups_folder)
    all_backups = []

    # Itera a través de cada cliente y obtiene sus respaldos
    for client in clients:
        client_backups_folder = os.path.join(backups_folder, client)
        backup_files = os.listdir(client_backups_folder)

        # Itera a través de cada archivo de respaldo y obtiene su información
        for backup_file in backup_files:
            file_path = os.path.join(client_backups_folder, backup_file)
            file_size = os.path.getsize(file_path)
            all_backups.append({"name": backup_file, "size": file_size, "owner": client})

    # Obtiene el número total de respaldos
    total_backups = len(all_backups)
    
    # Devuelve la lista de respaldos y el total en formato JSON
    return jsonify({"backups": all_backups, "total": total_backups}), 200
