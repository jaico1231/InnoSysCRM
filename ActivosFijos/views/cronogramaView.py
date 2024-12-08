from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ActivosFijos.forms.cronograma_form import CronogramaMantenimientoForm
from ActivosFijos.models.categoria_articulos import Categoria_Articulo
from ActivosFijos.models.cronograma import CronogramaMantenimiento
from shared.loggin import log_event

class Listar_CronogramaView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'ActivosFijos.view_cronograma'
    model = CronogramaMantenimiento
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cronograma Mantenimiento'
        context['entity'] = 'Cronograma'
        context['Btn_Add'] = [
            {
                'url':'ACTIVOS:Crear_Cronograma',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['GRUPO', 'FECHA PROGRAMADA', 'TIPO', 'DESCRIPCION', 'TERCERO']  # Encabezados de columnas
        context['fields'] = ['catArticulo', 'fecha_programada', 'tipo_mantenimiento', 'descripcion', 'tercero']  # Campos del modelo
        context['actions'] = [
            {
                'name': 'edit', 
                'label': '', 
                'icon': 'edit', 
                'color': 'secondary', 
                'color2': 'brown', 
                'url': 'ACTIVOS:Editar_Cronograma',
                'modal': 'Activa'
            },
            {
                'name': 'delete', 
                'label': '', 
                'icon': 'delete', 
                'color': 'danger',
                'color2': 'white', 
                'url': 'ACTIVOS:Eliminar_Cronograma',
                'modal': 'Activa'
            },
        ]
        return context
    
class Crear_CronogramaView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'ActivosFijos.add_cronograma'
    model = CronogramaMantenimiento
    form_class = CronogramaMantenimientoForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_Cronograma')

    def form_valid(self, form):
        cronograma = form.save(commit=False)
        nombre = form.cleaned_data['catArticulo']
        fecha_inicial = form.cleaned_data['fecha_programada']
        periocidad = form.cleaned_data['periocidad']
        fin_ano = date(fecha_inicial.year, 12, 31)
        
        # Generar cronogramas hasta el final del año
        cronogramas = []
        siguiente_fecha = fecha_inicial
        while siguiente_fecha <= fin_ano:
            cronogramas.append(
                CronogramaMantenimiento(
                    catArticulo=cronograma.catArticulo,
                    fecha_programada=siguiente_fecha,
                    tipo_mantenimiento=cronograma.tipo_mantenimiento,
                    descripcion=cronograma.descripcion,
                    tercero=cronograma.tercero,
                    periocidad=cronograma.periocidad,
                )
            )
            siguiente_fecha += timedelta(days=periocidad.CantidadDias)
        
        CronogramaMantenimiento.objects.bulk_create(cronogramas)
        log_event(self.request.user, 'info', f'Se creo el cronograma para {nombre} del año {datetime.now().year}..')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Cronograma'
        context['entity'] = 'Cronograma'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_Cronograma')
        return context
    
class Editar_CronogramaView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'ActivosFijos.change_cronograma'
    model = CronogramaMantenimiento
    form_class = CronogramaMantenimientoForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_Cronograma')

    def form_valid(self, form):
        cronograma = form.save(commit=False)
        cronograma.save()
        log_event(self.request.user, 'info', f'Se actualizo el cronograma. {cronograma.id}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cronograma'
        context['entity'] = 'Cronograma'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_Cronograma')
        return context
    
class Eliminar_CronogramaView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'ActivosFijos.delete_cronograma'
    model = CronogramaMantenimiento
    template_name = 'shared/del.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_Cronograma')
    
    def form_valid(self, form):
        cronograma = self.get_object()
        # cronograma = form.cleaned_data.get('catArticulo')
        log_event(self.request.user, 'info', f'Se elimino el cronograma {cronograma.catArticulo} con fecha {cronograma.fecha_programada}.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Cronograma'
        context['entity'] = 'Cronograma'
        context['texto'] = f'¿Desea eliminar el cronograma {self.object.id}?'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_Cronograma')
        return context