from configuracion.models.servicios import PaquetesServicios
from configuracion.forms.serviciosForm import PaquetesServiciosForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from shared.loggin import log_event

class RelacionesPaquetesListView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shared.view_paquetes_servicios'
    model = PaquetesServicios
    template_name = 'shared/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Relaciones de Paquetes'
        context['entity'] = 'Relaciones de Paquetes'        
        context['Btn_Add'] = [
            {
                'url':'configuracion:relacionespaquetescreate',
                'modal': 'Activar',
                }
                ]
        context['headers'] = [ 'CODIGO','PAQUETE', 'SERVICIO', 'ESTADO']
        context['fields'] = ['id', 'paquetes', 'servicios', 'estado']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'white',
                'url': 'configuracion:relacionespaquetesedit',
                'modal': 'Activar'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'configuracion:relacionespaquetesdel',
                'modal': 'Activar'
            },
        ]

class PaqueteServicioCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shared.view_paquetes_servicios'
    form_class = PaquetesServiciosForm
    template_name = 'shared/create.html'
    success_url = reverse_lazy('configuracion:listar_paquetes')

    def form_valid(self, form):
        # Aquí puedes realizar acciones adicionales al enviar el formulario,
        # como guardar el paquete y los servicios seleccionados.
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Relaciones de Paquetes'
        context['entity'] = 'Relaciones de Paquetes'
        context['list_url'] = 'configuracion:listar_paquetes'
        context['action'] = 'add'
        return context