# Sistema de repositorio centralizado de backups para bases de datos de servidores diferentes

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalados los siguientes componentes:

- **Python 3.9.16**.
- **MariaDB v10.6.12** o **PostgreSQL v14.7**.
- **Docker** (versión 19.03 o superior).
- **Docker Compose** (versión 3.8 o superior).
- **pip** (para instalar dependencias de Python).

---

## 1. Generación de datos de prueba

### Instalación de software

- **Python 3.9.16**: Verifica la versión instalada con el siguiente comando:
  ```bash
  python3 --version
  ```
  Si necesitas instalar Python 3.9.16:
  ```bash
  sudo apt update
  sudo apt install python3.9
  ```

- **MariaDB v10.6.12**: Sigue las instrucciones oficiales para instalar MariaDB.

- **PostgreSQL v14.7**: Sigue las instrucciones oficiales para instalar PostgreSQL.

### Instalación de dependencias de python

Ejecuta los siguientes comandos para instalar las dependencias necesarias:
```bash
pip install faker==18.6.2
pip install pymysql==1.0.3
pip install psycopg2==2.9.6
```

### Configuración de las bases de datos

**MariaDB**:
```sql
CREATE DATABASE tu_base_de_datos;
CREATE USER 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_contraseña';
GRANT ALL PRIVILEGES ON tu_base_de_datos.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;
```

**PostgreSQL**:
```sql
CREATE DATABASE tu_base_de_datos;
CREATE USER tu_usuario WITH ENCRYPTED PASSWORD 'tu_contraseña';
GRANT ALL PRIVILEGES ON DATABASE tu_base_de_datos TO tu_usuario;
```

### Generación de datos de prueba

Para generar datos de prueba, dirígete a la carpeta `client_fake_data_generator` y ejecuta uno de los siguientes scripts, dependiendo de la base de datos que estés utilizando:

```bash
python mariadb_fake_data_generator.py <config>
python postgresql_fake_data_generator.py <config>
```

Donde `<config>` puede ser `db1_config.json`, `db2_config.json` o `db3_config.json`.

---

## 2. Configuración

### Archivos `.env` del cliente

El proyecto incluye tres clientes predeterminados. Para agregar un nuevo cliente:

1. Crea una nueva carpeta en `./client/` (por ejemplo, `client4_app`).
2. Copia los archivos de un cliente existente (por ejemplo, `client1_app`) a la nueva carpeta.
3. Configura el archivo `.env` con los valores específicos del nuevo cliente.

Ejemplo de archivo `.env` del cliente:
```env
CLIENT_USERNAME=client1
CLIENT_APP_HOST=0.0.0.0
CLIENT_APP_PORT=5001
CENTRAL_API_RECEIVE_BACKUP_URL=http://localhost:5000/api/receive_backup
DB_HOST=0.0.0.0
DB_PORT=3306
DB_USER=test_user
DB_PASSWORD=test_password
DB_NAME=db1
DB_TYPE=mysql
BACKUP_DAY=2
BACKUP_HOUR=18
BACKUP_MINUTE=45
```

Para agregar el nuevo cliente al servicio de Docker, añade la siguiente sección en el archivo `docker-compose.yml`:
```yaml
  client4_app:
    build:
      context: ./client/client4_app
      dockerfile: Dockerfile
    env_file:
      - ./client/client4_app/.env
    network_mode: host
    depends_on:
      - server_app
    volumes:
      - ./client/client4_app/keys:/app/keys
      - ./client/client4_app/logs:/app/logs
      - ./client/client4_app/files:/app/files
    environment:
      - TZ=America/Santiago
```

### Configuración del servidor

El archivo `.env` del servidor tiene la siguiente estructura:
```env
SERVER_APP_HOST=0.0.0.0
SERVER_APP_PORT=5000
```

---

## 3. Despliegue

Antes de comenzar con el despliegue, asegúrate de que los archivos `.env` estén configurados correctamente en las siguientes rutas:
- `./server/server_app/.env`
- `./client/client1_app/.env`
- `./client/client2_app/.env`
- `./client/client3_app/.env`

### Compilación y Ejecución

1. Navega al directorio raíz del proyecto, donde se encuentra el archivo `docker-compose.yml`.
2. Ejecuta la compilación de los servicios:
   ```bash
   docker-compose build
   ```
3. Una vez completada la compilación, pon en marcha la aplicación con:
   ```bash
   docker-compose up -d
   ```
   Los servicios se ejecutarán en contenedores separados.

### Detener la aplicación

Para detener todos los servicios, ejecuta:
```bash
docker-compose down
```

### Frontend del servidor (administrador)

Accede al frontend del servidor en:
```
http://IP:3000/
```
Este interfaz permite visualizar y administrar los respaldos, incluidas las opciones de eliminación.

### Frontend del cliente

Accede al frontend de un cliente en:
```
http://IP:PORT/
```
En esta interfaz, podrás ver y desencriptar los respaldos almacenados.
