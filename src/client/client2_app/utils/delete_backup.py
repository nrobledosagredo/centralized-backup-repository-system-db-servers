import os

def delete_backup_file(file_path):
    # Intenta eliminar el archivo
    try:
        os.remove(file_path)
    except OSError as e:
        # Imprime un mensaje de error si no se pudo eliminar el archivo
        print(f"Error deleting file {file_path}: {e}")