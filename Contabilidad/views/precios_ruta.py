from Contabilidad.forms.iniciales_form import *
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from Contabilidad.models.retroactivo import Tabla_Precios_Rutas
from shared.loggin import log_event

class PreciosRutaView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('Contabilidad.view_tabla_precios_rutas',)
    model = Tabla_Precios_Rutas
    template_name = 'shared/list.html'
    context_object_name = 'precios_ruta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Precios Ruta'
        context['entity'] = 'Precios Ruta'
        context['Btn_Add'] = [
            {
                'url':'contabilidad:P_R_Create',
                'modal': 'Activar',
            }
        ]
        context['headers'] = [ 'Nombre','Distancia (Km)', 'Valor']
        context['fields'] = ['nombre','kmh', 'valor']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'contabilidad:P_R_Update',
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'contabilidad:P_R_Delete',
                # 'modal': '1'
            }
        ]
        return context
    
class CreatePreciosRutaView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('Contabilidad.add_tabla_precios_rutas',)
    model = Tabla_Precios_Rutas
    form_class = PreciosRutaForm
    template_name = 'shared/create.html'
    
    def get_success_url(self):
        if self.request.accepts('text/html/application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('contabilidad:precios_ruta_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request, 'info', f'Se agrego la ruta {form.instance.nombre} con el valor de {form.instance.precios}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Precios Ruta'
        context['entity'] = 'Precios Ruta'
        context['list_url'] = reverse_lazy('contabilidad:precios_ruta_list')
        return context

class UpdatePreciosRutaView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('Contabilidad.change_tabla_precios_rutas',)
    model = Tabla_Precios_Rutas
    form_class = PreciosRutaForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('text/html/application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('contabilidad:precios_ruta_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request, 'info', f'Se actualizo la ruta {form.instance.nombre} de {self.valor_actual} a {form.instance.valor}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Precios Ruta'
        context['entity'] = 'Precios Ruta'
        context['list_url'] = reverse_lazy('contabilidad:precios_ruta_list')
        self.valor = context['valor_actual']
        return context

class DeletePreciosRutaView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('Contabilidad.delete_tabla_precios_rutas',)
    model = Tabla_Precios_Rutas
    form_class = Tabla_Precios_Rutas
    template_name = 'shared/delete.html'

    def get_success_url(self):
        if self.request.accepts('text/html/application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('contabilidad:precios_ruta_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request, 'info', f'Se elimino la ruta {form.instance}')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Precios Ruta'
        context['entity'] = 'Precios Ruta'
        context['list_url'] = reverse_lazy('contabilidad:precios_ruta_list')
        return context