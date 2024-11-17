import threading
import time
from datetime import datetime, timedelta
import os
import sched

# Obtiene el día, la hora y el minuto de respaldo del archivo .env
backup_day = int(os.getenv('BACKUP_DAY'))
backup_hour = int(os.getenv('BACKUP_HOUR'))
backup_minute = int(os.getenv('BACKUP_MINUTE'))

def schedule_backup(backup_db):
    # Crea una instancia del scheduler
    s = sched.scheduler(time.time, time.sleep)

    def run_schedule():
        while True:
            # Realiza el respaldo
            backup_db()
            # Obtiene la hora actual
            now = datetime.now()
            # Calcula la fecha y la hora de la próxima tarea de respaldo
            next_backup = now.replace(hour=backup_hour, minute=backup_minute)
            # Si la próxima tarea de respaldo es anterior a la hora actual, añade 1 día
            if next_backup < now:
                next_backup += timedelta(days=1)
            # Si el día de la semana de la próxima tarea de respaldo no es el día de respaldo programado, avanza hasta el próximo día de respaldo
            while next_backup.weekday() != backup_day:
                next_backup += timedelta(days=1)
            # Calcula el intervalo hasta la próxima tarea de respaldo en segundos
            backup_interval = int((next_backup - now).total_seconds())
            # Programa la próxima tarea de respaldo
            s.enter(backup_interval, 1, backup_db)

            # Ejecuta el scheduler
            s.run()

    # Crea un hilo (thread) para ejecutar el scheduler
    t = threading.Thread(target=run_schedule)
    # Establece el hilo (thread) como hilo demonio
    t.daemon = True
    # Inicia el hilo (thread)
    t.start()