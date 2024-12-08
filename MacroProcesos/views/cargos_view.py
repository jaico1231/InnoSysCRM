from django.http import JsonResponse
from django.urls import reverse_lazy
from MacroProcesos.models.macroprocesos import Cargo_Macroprocesos
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from MacroProcesos.forms.macro_procesos_form import Cargo_Form
from shared.loggin import log_event

# Create your views here.

class Listar_Cargos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'MacroProcesos.view_macroprocesos'
    model = Cargo_Macroprocesos
    template_name= 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configuracion de Cargos'
        context['entity'] = 'Cargos'
        context['add_url'] = reverse_lazy('macroprocesos:Crear_Cargo')
        context['Btn_Add'] = [
            {
                'name':'add',
                'label':'Crear Cargos',
                'icon':'add',
                'url':'macroprocesos:Crear_Cargo',
                'modal': 'Activar',
                
            }
        ]
        context['headers'] = ['IDENTIFICADOR', 'CODIGO','CARGO', 'SECCION', 'TIPO DE CARGO']  
        context['fields'] = ['IdCargo', 'codigo', 'cargo', 'seccion_FK', 'tipo_personal_FK']
        context['actions'] = [
            {
                'name': 'edit', 
                'label': '', 
                'icon': 'edit', 
                'color': 'secondary', 
                'color2': 'brown', 
                'url': 'macroprocesos:Editar_Cargo',
                'modal': 'Activar',
            },
            {
                'name': 'delete', 
                'label': '', 
                'icon': 'delete', 
                'color': 'danger',
                'color2': 'white', 
                'url': 'macroprocesos:Eliminar_Cargo',
                'modal': 'Activar',
            },
            # Agrega más acciones aquí sea necesario
        ]
        return context

class Crear_Cargos(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'MacroProcesos.add_macroprocesos'
    model = Cargo_Macroprocesos
    form_class = Cargo_Form
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('macroprocesos:Listar_Cargo')
    
    def form_valid(self, form):
        cargo = form.cleaned_data.get('cargo')
        log_event(self.request.user, "info", f"Se Creo el cargo. {cargo}")
        return super().form_valid(form)    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Cargos'
        context['entity'] = 'Cargos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Cargo')
        return context

class Editar_Cargos(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'MacroProcesos.change_macroprocesos'
    model = Cargo_Macroprocesos
    form_class = Cargo_Form
    template_name = 'shared/create.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('macroprocesos:Listar_Cargo')
    
    def form_valid(self, form):
        cargo = form.cleaned_data.get('cargo')
        log_event(self.request.user, "info", f"Se Edito el cargo. {cargo}")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cargos'
        context['entity'] = 'Cargos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Cargo')
        return context
    
class Eliminar_Cargos(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'MacroProcesos.delete_macroprocesos'
    model = Cargo_Macroprocesos
    template_name = 'shared/del.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('macroprocesos:Listar_Cargo')

    def form_valid(self, form):
        cargo = form.cleaned_data.get('cargo')
        log_event(self.request.user, "info", f"Se Elimino el cargo. {cargo}")
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Cargos'
        context['entity'] = 'Cargos'
        context['texto'] = f'Seguro de eliminar el cargo {self.object.cargo}?'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Cargo')
        return context