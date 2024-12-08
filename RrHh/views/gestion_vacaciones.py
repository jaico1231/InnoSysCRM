from datetime import timedelta
import re, os
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from django.template.loader import get_template
from shared.global_utils import creacion_correos
from shared.models.datos_empresa import DatosIniciales
from shared.models.gestionemail import *
from shared.tasks import send_email_task
from RrHh.forms.gestion_vacaciones_form import *
from RrHh.models.hoja_vida import Hoja_Vida
from RrHh.models.vacaciones import Vacaciones
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from workdays import networkdays
now = datetime.datetime.now()


class Listar_Solicitudes_Vacaciones(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ['RrHh.view_vacaciones']
    model = Vacaciones
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filtrar las solicitudes de vacaciones según el rol del usuario
        if self.request.user.groups.filter(name='Colaborador').exists():
            colaborador = Hoja_Vida.objects.filter(numero_identificacion=self.request.user.NumeroIdentificacion).first()
            if colaborador:
                context['object_list'] = Vacaciones.objects.filter(colaborador_FK=colaborador)
            else:
                context['object_list'] = Vacaciones.objects.none()
        else:
            context['object_list'] = Vacaciones.objects.all()  # O cualquier otra lógica para otros roles

        grupos = self.request.user.groups.all()
        context['title'] = 'Solicitudes de Vacaciones'
        context['entity'] = 'Solicitudes'
        context['Btn_Add'] = [
            {
                'url': 'RrHh:Crear_Solicitud_Vacaciones',
                'modal': 'Activar',
            }
        ]

        headers, fields = [], []
        headers = ['SOLICITUD #', 'COLABORADOR', 'INICIO VACACIONES', 'DIAS SOLICITADOS', 'RETORNO LABORAL', 'JEFE INMEDIATO', 'ESTADO']
        fields = ['IdSolicitud', 'colaborador_FK', 'fecha_inicio_alternativa', 'dias', 'fecha_inicio_laboral', 'jefe_inmediato', 'estado']

        if self.request.user.groups.filter(name='Colaborador').exists():
            headers = ['SOLICITUD #',  'INICIO VACACIONES', 'DIAS SOLICITADOS', 'RETORNO LABORAL', 'ESTADO']
            fields = ['IdSolicitud',  'fecha_inicial', 'dias', 'fecha_final', 'estado']
        elif self.request.user.groups.filter(name='Jefe_Area').exists() or self.request.user.groups.filter(name='Administrador').exists():
            # Verificar el estado de cada solicitud en el object_list
            for solicitud in context['object_list']:
                if solicitud.estado.id == 3:
                    headers = ['SOLICITUD #', 'COLABORADOR', 'INICIO VACACIONES', 'DIAS SOLICITADOS', 'RETORNO LABORAL', 'JEFE INMEDIATO', 'ESTADO']
                    fields = ['IdSolicitud', 'colaborador_FK', 'fecha_inicio_alternativa', 'dias', 'fecha_inicio_laboral', 'jefe_inmediato', 'estado']
                    break  # Salir del bucle una vez que se haya encontrado un estado coincidente
                elif solicitud.estado.id == 1:
                    headers = ['SOLICITUD #', 'COLABORADOR', 'INICIO VACACIONES', 'DIAS SOLICITADOS', 'RETORNO LABORAL','JEFE INMEDIATO' ,'ESTADO']
                    fields = ['IdSolicitud', 'colaborador_FK', 'fecha_inicial', 'dias', 'fecha_final','estado']
                    break  # Salir del bucle una vez que se haya encontrado un estado coincidente

        context['headers'] = headers
        context['fields'] = fields    
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'white',
                'url': 'RrHh:Editar_Solicitud_Vacaciones',
            }
        ]
        
        return context
    
class Vacaciones_Create(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ['RrHh.view_vacaciones']
    template_name = 'shared/create.html'
    form_class = Solicitud_VacacionesForm
    success_url = reverse_lazy('RrHh:Lista_Solicitudes_Vacaciones')

    def form_valid(self, form):
        user = self.request.user.NumeroIdentificacion
        colaborador = Hoja_Vida.objects.filter(numero_identificacion=user).first()
        form.instance.colaborador_FK = colaborador
        form.instance.user_created = self.request.user
        dias_solicitados = networkdays(form.instance.fecha_inicial, form.instance.fecha_final)
        form.instance.dias = dias_solicitados
        fecha_final = form.instance.fecha_final 
        dia_laboral = fecha_final + timedelta(days=1)
        if dia_laboral.weekday() == 5 or dia_laboral.weekday() == 6:
            dia_laboral = dia_laboral + timedelta(days=1)
        form.instance.fecha_inicio_laboral = dia_laboral
        
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context.colaborador_FK_id = colaborador
        context['title'] = 'Solicitar vacaciones'
        context['entity'] = 'Solicitudes'
        context['list_url'] = reverse_lazy('RrHh:Lista_Solicitudes_Vacaciones')
        context['cancel_url'] = reverse_lazy('RrHh:Lista_Solicitudes_Vacaciones')
        return context

class Vacaciones_Edit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ['RrHh.view_vacaciones']
    model = Vacaciones
    template_name = 'vacaciones/editar_vacaciones.html'
    form_class = Gestion_VacacionesForm
    success_url = reverse_lazy('RrHh:Lista_Solicitudes_Vacaciones')

    def form_valid(self, form):
        # almacenamiento 
        numero_identificacion = form.instance.colaborador_FK.numero_identificacion
        numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
        doc = f'SOLICITUD_VACACIONES_{form.instance.IdSolicitud}.pdf'
        ruta = f'DOCUMENTOS/{numero_identificacion}/VACACIONES/{doc}'  # Asegúrate de definir correctamente la variable 'doc'
        ruta_completa = f"/ROMIL_BETA1/ROMIL_BETA1/static/assets/{ruta}"
        os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
        user_update = self.request.user
        if self.request.user.groups.filter(name='Jefe_de_area').exists():
            if form.instance.estado_id == 1:#pre aprobacion por jefe de area
                form.save()
            if form.instance.estado_id == 3:#reagendado
                dias_solicitados = networkdays(form.instance.fecha_inicio_alternativa, form.instance.fecha_fin_alternativa)
                form.instance.dias = dias_solicitados
        
        form.instance.file = ruta
        form.save()
        iniciales = DatosIniciales.objects.first()
        
        def get_dias_semana(fecha):
            dias_semana = {
                        0: "lunes",
                        1: "martes",
                        2: "miércoles",
                        3: "jueves",
                        4: "viernes",
                        5: "sábado",
                        6: "domingo"
                    }
            return dias_semana[fecha.weekday()]
        context = {
                 "razon_social" : iniciales.nombre,
                 "representante" : iniciales.representante_legal,
                 "cargo" : iniciales.cargo,
                 "fecha" : form.instance.updated_at,
                 "nombres" : form.instance.colaborador_FK.nombre,
                 "apellidos" : form.instance.colaborador_FK.apellido,
                 "tipo_doc": form.instance.colaborador_FK.tipo_documentoFK.Sigla,
                 "cedula": form.instance.colaborador_FK.numero_identificacion,
                 "fecha_inicio" : form.instance.fecha_inicial,
                 "fecha_final" : form.instance.fecha_final,
                 "year" : form.instance.created_at.year,
                 "fecha_final" : form.instance.fecha_final,
                 "dias" : form.instance.dias,
                 "fecha_solicitud" : form.instance.created_at,
                 "dia_letras" : get_dias_semana(form.instance.created_at),
                 "mes_solicitud" : form.instance.created_at.month,
                 "fecha_inicio_alternativa" : form.instance.fecha_inicio_alternativa,
                 "fecha_fin_alternativa" : form.instance.fecha_fin_alternativa,
                 "dias_alternativo" : form.instance.dias_alternativo,
                 "observaciones" : form.instance.observaciones,
                 "fecha_inicio_laboral" : form.instance.fecha_inicio_laboral,
                 "estado" : form.instance.estado_id
            }
        
        if form.instance.estado_id == 2:
            #aceptacion de solicitud de vacaciones
            template = get_template('cartas/Carta_Aceptacion_Vacaciones_Solicitud.html')
            
        elif form.instance.estado_id == 3:
            #rechazo de solicitud de vacaciones
            template = get_template('cartas/Carta_Rechazo_Vacaciones_Solicitud.html')
            
   
        html_template = template.render(context)
        if form.save():
            HTML(string=html_template).write_pdf(target=ruta_completa)
            # enviar correo con la carta adjunta 
            from django.core.mail import EmailMultiAlternatives
            from django.core.mail import get_connection
            subject, from_email, to_email = "Solicitud de Vacaciones", "app@in-sys.co", "jaico1231@gmail.com"
            text_content = "Cordial saludo."
            html_content = "<p>Por medio de la presente le informamos que su solicitud de vacaciones ha sido aceptada.<br>.</p>"
            html_content = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Respuesta de Solicitud</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }
                    .container {
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: #f9f9f9;
                    }
                    .header {
                        text-align: center;
                        margin-bottom: 20px;
                    }
                    .header h1 {
                        margin: 0;
                        font-size: 24px;
                        color: #0073e6;
                    }
                    .content {
                        margin-bottom: 20px;
                    }
                    .footer {
                        text-align: center;
                        font-size: 14px;
                        color: #777;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Respuesta de Solicitud</h1>
                    </div>
                    <div class="content">
                        <p>Cordial saludo,</p>
                        <p>Es un placer para nosotros informarle que su solicitud fue tramitada con éxito y su respuesta se encuentra en el siguiente archivo adjunto.</p>
                    </div>
                    <div class="footer">
                        <p>Gracias por confiar en nosotros.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            status=EstadoEmail.objects.get(pk=1)
        creacion_correos(subject,text_content,html_content,from_email,to_email,ruta_completa,status)
            
        
        # Llamar a la tarea asíncrona
        # send_email_task.delay(email_record.idemail)

        return super().form_valid(form)
                
           
            
            
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar solicitud'
        context['entity'] = 'Solicitudes'
        context['list_url'] = reverse_lazy('RrHh:Lista_Solicitudes_Vacaciones')
        context['cancel_url'] = reverse_lazy('RrHh:Lista_Solicitudes_Vacaciones')
        return context
    
class Historial_Vacaciones(LoginRequiredMixin,  PermissionRequiredMixin,TemplateView):    
    permission_required = ['RrHh.view_vacaciones']
    template_name = 'vacaciones/historial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hv = self.kwargs['pk']  # id de la hoja de vida

        # Obtén el año actual
        current_year = now.year

        # Filtra los registros de vacaciones del colaborador para el año actual
        listado_vacaciones = Vacaciones.objects.filter(
            colaborador_FK=hv, 
            fecha_inicial__year=current_year
        )

        # Inicializa los días disponibles de vacaciones
        dias_disponibles =15
        dias_tomados =0

        # Itera sobre cada registro de vacaciones y resta los días tomados
        for vacaciones in listado_vacaciones:
            
            dias_disponibles -= vacaciones.dias
            dias_tomados += vacaciones.dias or 0
        historial = Vacaciones.objects.filter(colaborador_FK=hv)
        context['historial'] = historial
        # Actualiza el contexto con la información necesaria
        context['year']= now.year
        context['dias_disponibles'] = dias_disponibles
        context['vacaciones'] = listado_vacaciones
        context['id_hv'] = hv        
        context['title'] = 'Historial Vacaciones'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')

        return context