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

The system is divided into separate client and server components, each with its own frontend and backend, ensuring flexibility and easy integration. This project is part of a distributed systems learning project, aimed at understanding the concepts of networked applications, data synchronization, and service orchestration in a real-world context. It was made for learning purposes.

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

### 1. Generate Test Data
1. **Install dependencies**  
   ```bash
   pip install faker==18.6.2 pymysql==1.0.3 psycopg2==2.9.6
   ```

2. **Create database & user**  
   - *MariaDB*:
     ```sql
     CREATE DATABASE your_db;
     CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
     GRANT ALL PRIVILEGES ON your_db.* TO 'user'@'localhost';
     ```
   - *PostgreSQL*:
     ```sql
     CREATE DATABASE your_db;
     CREATE USER user WITH PASSWORD 'password';
     GRANT ALL PRIVILEGES ON DATABASE your_db TO user;
     ```

3. **Generate sample data**  
   ```bash
   # From client_fake_data_generator folder
   python mariadb_fake_data_generator.py <config>
   # or
   python postgresql_fake_data_generator.py <config>
   ```
   *Replace `<config>` with `db1_config.json`, `db2_config.json`, or `db3_config.json`*

### 2. Configure Services
#### For Clients
1. **Add new client**:
   - Duplicate an existing client folder (e.g., `client1_app` → `client4_app`)
   - Update `.env` with your values:
     ```env
     CLIENT_USERNAME=client1
     CLIENT_APP_PORT=5001
     DB_HOST=0.0.0.0
     DB_PORT=3306
     DB_USER=test_user
     DB_PASSWORD=test_password
     BACKUP_SCHEDULE=2 18 45  # Day Hour Minute
     ```

2. **Add to Docker Compose**:
   ```yaml
   client4_app:
     build: ./client/client4_app
     env_file: ./client/client4_app/.env
     network_mode: host
     depends_on: [server_app]
     volumes: [...]
   ```

#### For Server
Create `.env` in `./server/server_app`:
```env
SERVER_APP_HOST=0.0.0.0
SERVER_APP_PORT=5000
```

### 3. Deploy
**Before starting**:  
Verify `.env` files exist in:
- Server folder
- All client folders

**Commands**:
```bash
# Build and start
docker-compose up --build -d

# Stop
docker-compose down
```

## Usage
- **Admin Interface**: `http://<IP>:3000`  
  *Manage all backups*
- **User Interface**: `http://<IP>:<CLIENT_PORT>`  
  *View/decrypt personal backups*
