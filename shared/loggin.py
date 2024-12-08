import os
import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def log_event(user, event_type, message):
    # Ruta del archivo de log
    log_file_path = 'event_logs.txt'
    
    # Crear o abrir el archivo de texto en modo 'append'
    with open(log_file_path, 'a') as log_file:
        # Crear el mensaje que se va a guardar
        log_message = f"{now} - User: {user}, Event Type: {event_type}, Message: {message}\n"
        # Escribir en el archivo de log
        log_file.write(log_message)
    
    print(f"Evento registrado: {log_message}")