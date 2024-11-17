import os
from cryptography.fernet import Fernet

# Crear la carpeta "keys" si no existe
if not os.path.exists("keys"):
    os.makedirs("keys")

def create_key():
    # Obtener el nombre de usuario de las variables de entorno
    username = os.getenv('CLIENT_USERNAME')
    # Crea una nueva clave de cifrado y la guarda en un archivo con el nombre del cliente
    key = Fernet.generate_key()
    with open(f"keys/{username}.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    # Obtener el nombre de usuario de las variables de entorno
    username = os.getenv('CLIENT_USERNAME')
    # Carga la clave de cifrado desde el archivo, si no existe, genera una nueva
    if not os.path.exists(f"keys/{username}.key"):
        return create_key()
    with open(f"keys/{username}.key", "rb") as key_file:
        key = key_file.read()
    return key

def encrypt_file(file_path):
    # Obtener el nombre de usuario de las variables de entorno
    username = os.getenv('CLIENT_USERNAME')
    # Agrega la extensión .enc al nombre del archivo original
    output_file_path = file_path + ".enc"

    # Carga la clave de cifrado y crea una instancia de Fernet
    key = load_key()
    fernet = Fernet(key)

    # Verifica si el archivo de entrada existe
    if not os.path.exists(file_path):
        print(f"El archivo de entrada {file_path} no existe")
        return None

    # Lee el contenido del archivo original
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Encripta el contenido del archivo
    encrypted_data = fernet.encrypt(file_data)

    # Escribe el contenido encriptado en un nuevo archivo con la extensión .enc
    with open(output_file_path, "wb") as file:
        file.write(encrypted_data)

    # Verifica si el archivo encriptado se creó correctamente
    if not os.path.exists(output_file_path):
        print(f"El archivo encriptado {output_file_path} no fue creado correctamente")
        return None
    else:
        print(f"El archivo encriptado {output_file_path} fue creado correctamente")

    # Retorna la ruta del archivo encriptado
    return output_file_path

def decrypt_file(file_path):
    # Obtener el nombre de usuario de las variables de entorno
    username = os.getenv('CLIENT_USERNAME')
    # Quita la extensión .enc del nombre del archivo original
    output_file_path = file_path.rsplit(".", 1)[0]  # Esto quitará la última extensión .enc

    # Carga la clave de cifrado y crea una instancia de Fernet
    key = load_key()
    fernet = Fernet(key)

    # Verifica si el archivo de entrada existe
    if not os.path.exists(file_path):
        print(f"El archivo de entrada {file_path} no existe")
        return None

    # Lee el contenido del archivo original
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Desencripta el contenido del archivo
    decrypted_data = fernet.decrypt(file_data)

    # Escribe el contenido desencriptado en un nuevo archivo sin la extensión .enc
    with open(output_file_path, "wb") as file:
        file.write(decrypted_data)

    # Verifica si el archivo desencriptado se creó correctamente
    if not os.path.exists(output_file_path):
        print(f"El archivo desencriptado {output_file_path} no fue creado correctamente")
        return None
    else:
        print(f"El archivo desencriptado {output_file_path} fue creado correctamente")

    # Retorna la ruta del archivo desencriptado
    return output_file_path