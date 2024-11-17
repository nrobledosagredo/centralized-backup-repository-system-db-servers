import gzip
import shutil

def compress_file(file_path):
    # Agrega la extensión '.gz' al nombre del archivo original
    compressed_file_path = f"{file_path}.gz"

    # Abre el archivo original en modo lectura binaria (rb)
    with open(file_path, "rb") as f_in:
        # Abre el archivo comprimido en modo escritura binaria (wb)
        with gzip.open(compressed_file_path, "wb") as f_out:
            # Copia el contenido del archivo original al archivo comprimido
            shutil.copyfileobj(f_in, f_out)

    # Retorna la ruta del archivo comprimido
    return compressed_file_path