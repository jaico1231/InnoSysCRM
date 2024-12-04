from django.core.mail import send_mail
from django.test import TestCase

def mes_en_letras_espanol(mes):
    meses = {
        'January': 'Enero',
        'February': 'Febrero',
        'March': 'Marzo',
        'April': 'Abril',
        'May': 'Mayo',
        'June': 'Junio',
        'July': 'Julio',
        'August': 'Agosto',
        'September': 'Septiembre',
        'October': 'Octubre',
        'November': 'Noviembre',
        'December': 'Diciembre'
    }
    return meses.get(mes, mes)

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


def send_email(request):
    subject = request.POST.get("subject", "")
    message = request.POST.get("message", "")
    from_email = request.POST.get("from_email", "")
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ["admin@example.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("/contact/thanks/")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse("Make sure all fields are entered and valid.")
    
from shared.models.gestionemail import Email
def creacion_correos(subject,text_content,html_content,from_email,to_email,ruta_completa,status):
    email_record = Email.objects.create(
        subject=subject,
        body_text=text_content,
        body_html=html_content,
        from_email=from_email,
        to_email=to_email,
        attachment_path=ruta_completa,
        status=status
    )
    return email_record

from shared.logging_config import logger

def log_event(level, message):
    """
    Función global para registrar eventos.

    Args:
        level (str): Nivel del log ('debug', 'info', 'warning', 'error', 'critical')
        message (str): Mensaje a registrar
    """
    log_function = getattr(logger, level, logger.info)
    log_function(message)