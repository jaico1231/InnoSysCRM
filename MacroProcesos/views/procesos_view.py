from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from MacroProcesos.forms.macro_procesos_form import Proceso_Form
from MacroProcesos.models.macroprocesos import *
from shared.loggin import log_event

# Create your views here.
class Listar_Procesos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'MacroProcesos.view_macroprocesos'
    model = Proceso
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configuracion de Procesos'
        context['entity'] = 'Procesos'
        context['Btn_Add'] = [
            {
                'name':'add',
                'label':'Crear Procesos',
                'icon':'add',
                'url':'macroprocesos:Crear_Procesos',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['IDENTIFICADOR', 'PROCESO', 'MACRO PROCESO']  # Encabezados de columnas
        context['fields'] = ['IdProceso', 'Proceso', 'macroprocesos_FK']  # Campos del modelo
        context['actions'] = [            
            {
                'name': 'edit', 
                'label': '', 
                'icon': 'edit', 
                'color': 'secondary', 
                'color2': 'brown', 
                'url': 'macroprocesos:Editar_Procesos'
            },
            {
                'name': 'delete', 
                'label': '', 
                'icon': 'delete', 
                'color': 'danger',
                'color2': 'white', 
                'url': 'macroprocesos:Eliminar_Procesos'
            },
            # Agrega más acciones aquí sea necesario
        ]
        return context

class Crear_Procesos(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'MacroProcesos.add_macroprocesos'
    model = Proceso
    form_class = Proceso_Form
    template_name = 'shared/create.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('macroprocesos:Listar_Procesos')

    def form_valid(self, form):
        proceso = form.cleaned_data.get('Proceso')
        log_event(self.request.user, "info", f"Se Creo el Procesos. {proceso}")
        return super().form_valid(form)
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Procesos'
        context['entity'] = 'Procesos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Procesos')
        return context

class Editar_Procesos(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'MacroProcesos.change_macroprocesos'
    model = Proceso
    form_class = Proceso_Form
    template_name = 'shared/create.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('macroprocesos:Listar_Procesos')

    def form_valid(self, form):
        proceso = form.cleaned_data.get('Proceso')
        log_event(self.request.user, "info", f"Se Edito el Procesos. {proceso}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Procesos'
        context['entity'] = 'Procesos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Procesos')
        return context
    
class Eliminar_Procesos(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'MacroProcesos.delete_macroprocesos'
    model = Proceso
    template_name = 'shared/del.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('macroprocesos:Listar_Procesos')

    def form_valid(self, form):
        proceso = self.get_object()
        log_event(self.request.user, "info", f"Se Elimino el Procesos. {proceso}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Procesos'
        context['entity'] = 'Procesos'
        context['texto'] = f'¿Seguro de eliminar el Procesos {self.object.Proceso}?'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Procesos')
        return context
    
