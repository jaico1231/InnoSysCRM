from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ActivosFijos.forms.cronograma_form import BitacoraMantenimientoForm
from ActivosFijos.models.cronograma import CronogramaMantenimiento,BitacoraMantenimiento
from shared.loggin import log_event

class Listar_BitacoraView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'ActivosFijos.view_bitacora'
    model = BitacoraMantenimiento
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mantenimiento'
        context['entity'] = 'Mantenimiento'
        context['Btn_Add'] = [
            {
                'url':'ACTIVOS:Crear_Bit',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['CODIGO', 'ARTICULO', 'GRUPO','FECHA REAIZADA', 'TIPO', 'TERCERO']  # Encabezados de columnas
        context['fields'] = ['articulo.codigo', 'articulo', 'articulo__GrupoArticulo_FK', 'created_at', 'tipomantenimiento' ,'tercero']  # Campos del modelo
        context['actions'] = [
            {
                'name': 'edit', 
                'label': '',
                'icon': 'edit', 
                'color': 'secondary', 
                'color2': 'brown', 
                'url': 'ACTIVOS:Editar_Bit',
                'modal': 'Activa'
            },
            {
                'name': 'delete', 
                'label': '', 
                'icon': 'delete', 
                'color': 'danger',
                'color2': 'white', 
                'url': 'ACTIVOS:Borrar_Bit',
                'modal': 'Activa'
            },
        ]
        return context

class Crear_BitacoraView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'ActivosFijos.add_bitacora'
    model = BitacoraMantenimiento
    form_class = BitacoraMantenimientoForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_Bit')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Bitacora Mantenimiento'
        context['entity'] = 'Crear Bitacora'
        context['list_url'] = 'ACTIVOS:Listar_Bit'
        return context

class Editar_BitacoraView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'ActivosFijos.change_bitacora'
    model = BitacoraMantenimiento
    form_class = BitacoraMantenimientoForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_Bit')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Bitacora Mantenimiento'
        context['entity'] = 'Editar Bitacora'
        context['list_url'] = 'ACTIVOS:Listar_Bit'
        return context

class Borrar_BitacoraView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'ActivosFijos.delete_bitacora'
    model = BitacoraMantenimiento
    template_name = 'shared/delete.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_Bit')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Bitacora Mantenimiento'
        context['entity'] = 'Borrar Bitacora'
        context['texto'] = f'¿Estas seguro de borrar la bitacora ?'
        context['list_url'] = 'ACTIVOS:Listar_Bit'
        return context
    
class IndicadorCronogramaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'ActivosFijos.view_cronograma'
    template_name = 'indicadores/indicadores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todos los cronogramas del año vigente
        current_year = datetime.now().year
        cronogramas = CronogramaMantenimiento.objects.filter(fecha_programada__year=current_year)

        # Inicializar datos para la matriz de cumplimiento mensual
        matriz_cumplimiento = {}
        porcentaje_anual = {}

        for cronograma in cronogramas:
            articulo = cronograma.catArticulo
            print(articulo)
            grupo = articulo.GrupoArticulo_FK
            if grupo not in matriz_cumplimiento:
                matriz_cumplimiento[grupo] = {month: 0 for month in range(1, 13)}
                porcentaje_anual[grupo] = 0

            for month in range(1, 13):
                # Verificar si el mantenimiento se realizó en el mes específico
                if BitacoraMantenimiento.objects.filter(
                    articulo__GrupoArticulo_FK=grupo,
                    fecha_realizacion__year=current_year,
                    fecha_realizacion__month=month
                ).exists():
                    matriz_cumplimiento[grupo][month] += 1

        # Calcular el porcentaje anual de cumplimiento
        for grupo, meses in matriz_cumplimiento.items():
            total_mantenimientos = sum(meses.values())
            total_programados = cronogramas.filter(catArticulo__GrupoArticulo_FK=grupo).count()
            porcentaje_anual[grupo] = (total_mantenimientos / total_programados) * 100 if total_programados else 0

        context['matriz_cumplimiento'] = matriz_cumplimiento
        context['porcentaje_anual'] = porcentaje_anual
        context['title'] = 'Indicador del Cronograma de Mantenimiento'
        context['entity'] = 'Cronograma de Mantenimiento'

        return context