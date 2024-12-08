# tasks.py en tu aplicación

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from shared.models.gestionemail import *
from django.core.exceptions import ObjectDoesNotExist
import logging

# Configura el logger
logger = logging.getLogger(__name__)

@shared_task
def send_email_task():
    correos = Email.objects.filter(status=1 or 3)
    for email_record in correos:   
        try:
            msg = EmailMultiAlternatives(
                email_record.subject,
                email_record.body_text,
                email_record.from_email,
                [email_record.to_email]
            )
            if email_record.body_html:
                msg.attach_alternative(email_record.body_html, "text/html")
            if email_record.attachment_path:
                msg.attach_file(email_record.attachment_path)
            msg.send()
            email_record.status = EstadoEmail.objects.get(pk=2)  # Enviado
        except Exception as e:
            email_record.status = EstadoEmail.objects.get(pk=3) # Fallido
            print(f"Error al enviar el correo: {e}")
        finally:
            email_record.save()
# Para ejecutar automaticamente: celery -A ROMIL_01 worker --loglevel=info



import threading
import time
from django.http import HttpResponse

def background_task():
    while True:
        # Aquí va el código que quieres ejecutar continuamente
        print("Ejecutando tarea en segundo plano...")
        time.sleep(10)  # Espera 10 segundos antes de volver a ejecutar la tarea

def mi_vista(request):
    # Crear y empezar el hilo
    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()

    return HttpResponse('Tarea en segundo plano iniciada.')
