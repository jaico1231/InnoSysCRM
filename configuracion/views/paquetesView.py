from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from configuracion.forms.serviciosForm import PaquetesForm, PaquetesServiciosForm
from configuracion.models.servicios import Paquetes, PaquetesServicios
from django.urls import  reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from shared.loggin import log_event
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
class TogglePaqueteEstadoView(LoginRequiredMixin, UpdateView):
    model = Paquetes
    fields = ['estado']
    success_url = reverse_lazy('configuracion:paqueteslist')

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        paquete = get_object_or_404(Paquetes, pk=kwargs['pk'])
        
        # Invertir el estado de 'activo' o 'estado'
        paquete.estado = not paquete.estado
        paquete.save()
        x = Paquetes.objects.filter(pk=paquete.pk).update(estado=paquete.estado)
        log_event(request.user, 'Paquete', f'se cambio el estado del Paquete {paquete.codigo} a {paquete.estado}', )
        

        return JsonResponse({'success': True, 'estado': paquete.estado})
      

class PaquetesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'shared.view_paquetes'
    model = Paquetes
    template_name = 'shared/list_estado.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Paquetes'
        context['entity'] = 'Paquetes'        
        context['Btn_Add'] = [
            {
                'name': 'add',
                'label': 'Crear Paquete',
                'icon': 'add',
                'url':'configuracion:paquetescreate',
                'modal': 'Activar',                
                }
                ]
        context['url_toggle'] = 'configuracion:estadopaquete'
        
        context['headers'] = [ 'CODIGO','PAQUETE', 'PRECIO', 'ESTADO']
        context['fields'] = ['codigo', 'nombre', 'precio']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'white',
                'url': 'configuracion:paquetesedit',
                'modal': 'Activar'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'configuracion:paquetesdel',
                'modal': 'Activar'
            },
        ]
        return context
# encuentra la forma de acerlo con  creates/paquetes.html
class PaquetesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shared.add_paquetes'
    model = Paquetes
    template_name = 'shared/create.html'
    form_class = PaquetesServiciosForm
    success_message = "El paquete se creó con éxito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        return reverse_lazy('configuracion:paqueteslist')

    def form_valid(self, form):
        # Guardar el paquete
        paquete = form.save()
        servicios = form.cleaned_data['servicios']

        # Sumar los precios de los servicios seleccionados
        total_precio = sum(servicio.precio for servicio in servicios)
        paquete.precio = total_precio
        paquete.save() 
        # Agregar los servicios seleccionados al paquete
        for servicio in servicios:
            PaquetesServicios.objects.create(paquete=paquete, servicio=servicio)
        x = self.get_object()
        messages.success(self.request, self.success_message)
        log_event(self.request.user, 'info', f'Se creo el paquete {x}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Paquetes'
        context['entity'] = 'Paquetes'
        context['list_url'] = 'configuracion:paqueteslist'
        context['action'] = 'add'
        return context

    
class PaquetesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shared.change_paquetes'
    model = Paquetes
    template_name = 'shared/create.html'
    form_class = PaquetesServiciosForm
    success_message = "Se actualizo con exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        return reverse_lazy('configuracion:paqueteslist')

    def form_valid(self, form):
        paquete = form.save()
        servicios = form.cleaned_data['servicios']

        # Agregar los servicios seleccionados al paquete
        for servicio in servicios:
            PaquetesServicios.objects.create(paquete=paquete, servicio=servicio)
        x = self.get_object()
        messages.success(self.request, self.success_message)
        log_event(self.request.user, 'info', f'Se actualizo el paquete {x}')
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Paquetes'
        context['entity'] = 'Paquetes'
        context['list_url'] = 'configuracion:paqueteslist'
        context['action'] = 'edit'
        return context
    
class PaquetesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'shared.delete_paquetes'
    model = Paquetes
    template_name = 'shared/del.html'

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': 'Se elimino con exito'})
        return reverse_lazy('configuracion:paqueteslist')

    def form_valid(self, form):
        x= self.get_object()
        messages.success(self.request, 'Se elimino con exito')
        log_event(self.request.user, 'info', f'Paquetes {x.nombre}')
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Paquetes'
        context['entity'] = 'Paquetes'
        context['texto'] = f' ¿Estas seguro de eliminar el Paquetes {self.object} ?'
        context['list_url'] = 'configuracion:paqueteslist'
        return context