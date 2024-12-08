import datetime
from email.message import EmailMessage
from django.urls import reverse_lazy
from io import BytesIO
import os
import tempfile
from django.http import FileResponse, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from RrHh.forms.permiso_laboralform import Permiso_Laboral_AutorizarForm, Permiso_Laboral_EmpleadoForm
from RrHh.models.permiso_laboral import Permiso_Laboral
from RrHh.models.hoja_vida import Hoja_Vida
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView
from django.template.loader import get_template
from weasyprint import HTML
from shared.loggin import log_event
now = datetime.datetime.now()


# agrega decorador login_required a la vista
class Listar_Solicitudes_Permiso( ListView):
    model = Permiso_Laboral
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Solicitudes Permiso'
        context['entity'] = 'Solicitudes'
        context['Btn_Add'] = [
            {
                'url':'RrHh:Crear_Solicitud_permiso_laboral',
                'modal': 'Activar',
                }
        ]
        context['headers'] = ['PERMISO #', 'EMPLEADO', 'TIPO DE PERMISO', 'FECHA SOLICITUD', 'ESTADO', 'AUTORIZADO POR', 'FECHA AUTORIZACIÓN']
        context['fields'] = ['IdPermiso', 'solicitante_FK', 'tipo_permisoFK', 'fecha_solicitada', 'estado_FK', 'autorizador', 'fecha_autorizacion']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'RrHh:Editar_Solicitud_permiso_laboral',
                'modal': '1'
            },
            {
                'name': 'print',
                'label': '',
                'icon': 'print',
                'color': 'success',
                'color2': 'white',
                'url': 'RrHh:imprimir_SP',
                'modal': '1'
            }
        ]
        context['list_url'] = reverse_lazy('RrHh:Listar_Solicitudes_Permiso')
        context['add_url'] = reverse_lazy('RrHh:Crear_Solicitud_permiso_laboral')
        return context

# class Listar_Solicitudes_Permiso(LoginRequiredMixin,  ListView):
#     # permission_required = 'RrHh.view_novedadnomina'
#     model = Permiso_Laboral
#     template_name = 'shared/list.html'

#     # def get_template_names(self):
#     #     if self.request.user.groups.filter(name='Colaborador').exists():
#     #         return ['solicitudes/Listar_solicitud_Permiso_colaborador.html']
#     #     else:
#     #         return ['solicitudes/Listar_solicitud_Permiso.html']

#     def get_context_data(self, **kwargs):    
#         context = super().get_context_data(**kwargs)
#         if self.request.user.groups.filter(name='Colaborador').exists():
#             colaborador = Hoja_Vida.objects.filter(numero_identificacion=self.request.user.NumeroIdentificacion).first()
           
#             if colaborador:
#                 context['lista'] = Permiso_Laboral.objects.filter(solicitante_FK=colaborador)
#             else:
#                 context['lista'] = Permiso_Laboral.objects.none()
#         else:
            
#             context['lista'] = Permiso_Laboral.objects.all()

#         context['title'] = 'Listar Permisos Laborales'
#         context['entity'] = 'Solicitudes'
#         context['add_url'] = reverse_lazy('RrHh:Crear_Solicitud_permiso_laboral')
#         context['Btn_Add'] = [
#             {
#                 'url':'RrHh:Crear_Solicitud_permiso_laboral',
#                 'modal': 'Activar',
#                 }
#         ]
#         context['headers'] = ['PERMISO #', 'EMPLEADO', 'TIPO DE PERMISO', 'FECHA SOLICITUD', 'ESTADO', 'AUTORIZADO POR', 'FECHA AUTORIZACIÓN']
#         context['fields'] = ['IdPermiso', 'solicitante_FK', 'tipo_permisoFK', 'fecha_solicitada', 'estado_FK', 'autorizador', 'fecha_autorizacion']
#         context['actions'] = [
#             {
#                 'name': 'edit',
#                 'label': '',
#                 'icon': 'edit',
#                 'color': 'secondary',
#                 'color2': 'brown',
#                 'url': 'RrHh:Editar_Solicitud_permiso_laboral',
#                 'modal': '1'
#             },
#             {
#                 'name': 'print',
#                 'label': '',
#                 'icon': 'print',
#                 'color': 'success',
#                 'color2': 'white',
#                 'url': 'RrHh:imprimir_SP',
#                 'modal': '1'
#             }
#         ]
#         return context

class Crear_Permiso_Laboral(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ['RrHh.view_permiso_laboral']
    template_name = 'shared/create.html'
    form_class = Permiso_Laboral_EmpleadoForm
    
    def get_success_url(self):
        if self.request.accepts('aplication/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('RrHh:Listar_Solicitudes_Permisos')
                

    def form_valid(self, form):
        form.instance.solicitante_FK = Hoja_Vida.objects.get(numero_identificacion=self.request.user.NumeroIdentificacion)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Solicitud'
        context['entity'] = 'Solicitud'
        context['list_url'] = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')
        return context

# @method_decorator(csrf_exempt, name='dispatch')    
class Permiso_Laboral_Edit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ['RrHh.view_permiso_laboral']
    model = Permiso_Laboral
    template_name = 'solicitudes/autorizacion_solicitud.html'
    form_class = Permiso_Laboral_AutorizarForm
    success_url = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')

  
    def form_valid(self, form):
        form.instance.autorizador = self.request.user
        form.instance.fecha_autorizacion = datetime.datetime.now()
        form.save()
        context = self.get_context_data()
        template = get_template('cartas/Carta_Aceptacion_Vacaciones_Solicitud.html')
        html_template = template.render(context)

        # Generar el PDF en memoria
        pdf_buffer = BytesIO()
        HTML(string=html_template).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        if 'print' in self.request.POST:
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="Permiso_Laboral.pdf"'
            return response

        elif 'mail' in self.request.POST:
            email = EmailMessage(
                'Asunto del correo',
                'Cuerpo del correo.',
                'from@example.com',
                ['to@example.com'],
            )
            email.attach('Permiso_Laboral.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send()
            return HttpResponse("Correo enviado con éxito")

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Autorización de solicitud'
        context['entity'] = 'Solicitudes'
        context['list_url'] = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')
        return context

class Permiso_Laboral_Delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ['RrHh.view_permiso_laboral']
    model = Permiso_Laboral
    template_name = 'shared/del.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('RrHh:Listar_Solicitudes_Permisos')

    def post(self, request, *args, **kwargs):
        log_event(self.request.user, "info", f"Se elimino la solicitud de permisos laborales numero {self.object.IdPermiso}.")
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar solicitud'
        context['entity'] = 'Solicitudes'
        context['texto'] = f'Seguro de eliminar la solicitud de permisos laborales {self.object.IdPermiso}?'
        context['list_url'] = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')
        return context
    
    
class print_permiso_laboral(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ['RrHh.view_permiso_laboral']
    model = Permiso_Laboral
    template_name = 'solicitudes/autorizacion_solicitud.html'
    form_class = Permiso_Laboral_AutorizarForm
    success_url = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Autorización de solicitud'
        context['entity'] = 'Solicitudes'
        context['list_url'] = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')
        return context
    
class Imprimir_Permiso_Laboral(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ['RrHh.view_permiso_laboral']
    template_name = 'cartas/Carta_Aceptacion_Vacaciones_Solicitud.html'
    model = Permiso_Laboral
    form_class = Permiso_Laboral_AutorizarForm
    success_url = reverse_lazy('RrHh:Listar_Solicitudes_Permisos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context

class Historial_Permiso_Laboral(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ['RrHh.view_permiso_laboral']
    model = Permiso_Laboral
    template_name = 'solicitudes/historial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hv = self.kwargs['pk']
        periodo = self.request.GET.get('periodo', 'anual')

        # Definir el rango de fechas según el período seleccionado
        if periodo == 'anual':
            fecha_inicio = now - datetime.timedelta(days=365)
        elif periodo == 'semestral':
            fecha_inicio = now - datetime.timedelta(days=6 * 30)  # Aproximadamente 6 meses
        elif periodo == 'trimestral':
            fecha_inicio = now - datetime.timedelta(days=3 * 30)  # Aproximadamente 3 meses
        elif periodo == 'total':
            fecha_inicio = None  # No filtrar por fecha
        else:
            raise ValueError("El periodo seleccionado no es válido")

        # Filtrar permisos según el rango de fechas
        if fecha_inicio:
            context['permiso_por_ano'] = Permiso_Laboral.objects.filter(solicitante_FK=hv, fecha_solicitada__range=(fecha_inicio, now))
        else:
            context['permiso_por_ano'] = Permiso_Laboral.objects.filter(solicitante_FK=hv)

        # Añadir información adicional al contexto
        context['id_hv'] = hv
        context['title'] = 'Historial de Permisos Laborales'
        context['entity'] = 'Solicitudes'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        context['create_url'] = reverse_lazy('RrHh:Crear_Solicitudes')
        return context
    


      # def form_valid(self, form):
    #     form.instance.autorizador = self.request.user
    #     form.instance.fecha_autorizacion = datetime.datetime.now()
    #     form.save()
    #     numero_identificacion = form.instance.solicitante_FK.numero_identificacion
    #     doc = f'Permiso_Laboral_{self.object.IdPermiso}.pdf'
    #     ruta = f'DOCUMENTOS/{numero_identificacion}/PERMISOS/{doc}'
    #     ruta_completa = f"/ROMIL_BETA1/ROMIL_BETA1/static/assets/{ruta}"
    #     os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)

    #     context = self.get_context_data()
    #     template = get_template('cartas/Carta_Aceptacion_Vacaciones_Solicitud.html')
    #     html_template = template.render(context)
    #     pdf_buffer = BytesIO()
    #     HTML(string=html_template).write_pdf(pdf_buffer)
    #     pdf_buffer.seek(0)

    #     if 'print' in self.request.POST:
    #         print("Imprimiendo...")
    #         return FileResponse(pdf_buffer, as_attachment=False, filename='Permiso_Laboral.pdf')
                
            
    #     elif 'mail' in self.request.POST:
    #         email = EmailMessage(
    #             'Asunto del correo',
    #             'Cuerpo del correo.',
    #             'from@example.com',
    #             ['to@example.com'],
    #         )
    #         email.attach_file(ruta_completa)
    #         email.send()
    #         return HttpResponse("Correo enviado con éxito")

