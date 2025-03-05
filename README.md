# Centralized backup repository system for databases across different servers

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Overview

This project is a centralized backup repository system designed for managing database backups across different servers. It leverages technologies such as MariaDB, PostgreSQL, Docker, Flask, and React to provide a scalable and secure solution for database management. 

The system is divided into separate client and server components, each with its own frontend and backend, ensuring flexibility and easy integration. This project is part of a distributed systems learning project, aimed at understanding the concepts of networked applications, data synchronization, and service orchestration in a real-world context.

## Features

- **Centralized backup management**: Securely store and manage backups from multiple databases across different servers.
- **Multi-database support**: Compatible with MariaDB and PostgreSQL databases.
- **Automated backups**: Schedule backups at specific intervals using client configurations.
- **User and admin interfaces**: Separate frontends for users and administrators to manage and view backups.
- **Dockerized deployment**: Easy deployment using Docker and Docker Compose.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.9.x**
- **MariaDB v10.6.12** or **PostgreSQL v14.7**
- **Docker** (version 19.03 or higher)
- **Docker Compose** (version 3.8 or higher)
- **pip** (for installing Python dependencies)

## Setup

### 1. Generate test data

To generate test data for your databases, follow these steps:

1. Install the required Python dependencies:
   ```bash
   pip install faker==18.6.2 pymysql==1.0.3 psycopg2==2.9.6
   ```

2. Set up your database:
   - **MariaDB**:
     ```sql
     CREATE DATABASE your_database;
     CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
     GRANT ALL PRIVILEGES ON your_database.* TO 'your_user'@'localhost';
     FLUSH PRIVILEGES;
     ```
   - **PostgreSQL**:
     ```sql
     CREATE DATABASE your_database;
     CREATE USER your_user WITH ENCRYPTED PASSWORD 'your_password';
     GRANT ALL PRIVILEGES ON DATABASE your_database TO your_user;
     ```

3. Navigate to the `client_fake_data_generator` folder and run the appropriate script for your database:
   ```bash
   python mariadb_fake_data_generator.py <config>
   # OR
   python postgresql_fake_data_generator.py <config>
   ```
   Replace `<config>` with `db1_config.json`, `db2_config.json`, or `db3_config.json`.

### 2. Configuration

#### Client configuration

The project includes three predefined clients (users). To add a new client:

1. Create a new folder under `./client/` (e.g., `client4_app`).
2. Copy the files from an existing client (e.g., `client1_app`) into the new folder.
3. Configure the `.env` file with the specific values for the new client.

Example of a client’s `.env` file:
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

4. Add the new client to the `docker-compose.yml` file:
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

#### Server configuration

The server `.env` file should have the following structure:
```env
SERVER_APP_HOST=0.0.0.0
SERVER_APP_PORT=5000
```

### 3. Deployment

Before starting the deployment, ensure that the `.env` files are correctly configured at the following paths:
- `./server/server_app/.env`
- `./client/client1_app/.env`
- `./client/client2_app/.env`
- `./client/client3_app/.env`

#### Build and run

1. Navigate to the root directory of the project, where the `docker-compose.yml` file is located.
2. Build the services:
   ```bash
   docker-compose build
   ```
3. Start the application:
   ```bash
   docker-compose up -d
   ```
   The services will now run in separate containers.

#### Stop the application

To stop all services, run:
```bash
docker-compose down
```

## Usage

### Administrator frontend

Access the administrator frontend at:
```
http://IP:3000/
```
This interface provides administrators with full control to view, manage, and delete backups.

### User frontend

Access the user frontend at:
```
http://IP:PORT/
```
This interface allows users to securely view and decrypt their backups.
