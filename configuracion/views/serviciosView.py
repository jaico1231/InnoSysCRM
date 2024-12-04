from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import  HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from shared.loggin import log_event
from configuracion.models.servicios import Servicios
from configuracion.forms.serviciosForm import ServiciosForm, PaquetesForm,  MedicosForm, Medico_paquetesForm
from shared.views.tercerosView import TercerosCreateView

from django.apps import apps
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

class ServiciosListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'shared.view_servicios'
    model = Servicios
    template_name = 'shared/list_estado.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Servicios'
        context['entity'] = 'Servicios'        
        context['Btn_Add'] = [
            {   
                'name': 'add',
                'label': 'Crear Servicio',
                'url':'configuracion:servicioscreate',
                'modal': 'Activar',
                }
                
                ]
        context['url_toggle'] = 'configuracion:estadoservicio'
        context['headers'] = [ 'CODIGO','SERVICIO', 'PRECIO', 'ESTADO']
        context['fields'] = ['codigo', 'nombre', 'precio', ]
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'white',
                'url': 'configuracion:serviciosedit',
                'modal': 'Activar'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'configuracion:serviciosdel',
                'modal': 'Activar'
            },
        ]
        return context
      
class ToggleServicioEstadoView(LoginRequiredMixin, UpdateView):
    model = Servicios
    fields = ['estado']
    success_url = reverse_lazy('configuracion:servicioslist')

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        servicio = get_object_or_404(Servicios, pk=kwargs['pk'])
        # Invertir el estado de 'activo' o 'estado'
        servicio.estado = not servicio.estado
        servicio.save()
        x = Servicios.objects.get(id=servicio.id)
        log_event(request.user, 'servicio', f'se cambio el estado del servicio {servicio.codigo} a {servicio.estado}', )
        print(f'Nuevo estado de servicio {servicio.id}: {servicio.estado}')  # Añadir un log para verificar el cambio
        return JsonResponse({'success': True, 'estado': servicio.estado})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Activar Servicio'
        context['entity'] = 'Servicio'
        context['list_url'] = 'configuracion:servicioslist'
        return context
    
    

class ServiciosCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shared.add_servicios'
    model = Servicios
    template_name = 'shared/create.html'
    form_class = ServiciosForm
    success_message = "Se creó con éxito"

    def get_success_url(self):
        return reverse_lazy('servicioslist')

    def form_valid(self, form):
        # Guardar el objeto antes de obtener el nombre
        servicio = form.save()
        messages.success(self.request, self.success_message)
        log_event(self.request.user, 'info', f'Se agregó el Servicio {servicio.nombre}')
        
        # Verificar si la solicitud es AJAX
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('configuracion:servicioslist')
        context['cancel_url'] = reverse_lazy('configuracion:servicioslist')
        context['action'] = 'add'
        return context

class ServiciosUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shared.change_servicios'
    model = Servicios
    template_name = 'shared/create.html'
    form_class = ServiciosForm
    success_message = "Se actualizó con éxito"

    def get_success_url(self):
        return reverse_lazy('configuracion:servicioslist')

    def form_valid(self, form):
        servicio = form.save()
        messages.success(self.request, self.success_message)
        log_event(self.request.user, 'info', f'Se actualizó el Servicio {servicio.nombre}')
        
        # Verificar si la solicitud es AJAX
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('configuracion:servicioslist')
        context['cancel_url'] = reverse_lazy('configuracion:servicioslist')
        context['action'] = 'edit'
        return context

class ServiciosDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'shared.delete_servicios'
    model = Servicios
    template_name = 'shared/del.html'

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('configuracion:servicioslist')

    def form_valid(self, form):
        x = self.get_object()
        messages.success(self.request, 'Se elimino con exito')
        log_event(self.request.user, 'info', f'Se elimino el Servicio {x.nombre}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Servicio'
        context['entity'] = 'Servicios'
        context['texto'] = f'Seguro de eliminar el Servicio {self.object.nombre}?'
        context['list_url'] = reverse_lazy('configuracion:servicioslist')
        return context