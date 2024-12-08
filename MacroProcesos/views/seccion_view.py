from urllib import response
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from MacroProcesos.models.macroprocesos import *
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from MacroProcesos.forms.macro_procesos_form import Seccion_Form
from shared.loggin import log_event

class Listar_Seccion(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'MacroProcesos.view_macroprocesos'
    model = Seccion
    template_name = 'shared/list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configuracion de Seccion'
        context['entity'] = 'Seccion'
        context['Btn_Add'] = [
            {
                'name':'add',
                'label':'Crear Seccion',
                'icon':'add',
                'url':'macroprocesos:Crear_Seccion',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['IDENTIFICADOR', 'SECCION']  # Encabezados de columnas
        context['fields'] = ['IdSeccion', 'Seccion']  # Campos del modelo
        context['actions'] = [            
            {
                'name': 'edit', 
                'label': '', 
                'icon': 'edit', 
                'color': 'secondary', 
                'color2': 'brown', 
                'url': 'macroprocesos:Editar_Seccion',
                'modal': 'Activar',
            },
            {
                'name': 'delete', 
                'label': '', 
                'icon': 'delete', 
                'color': 'danger',
                'color2': 'white', 
                'url': 'macroprocesos:Eliminar_Seccion',
                'modal': 'Activar',
            },
            # Agrega más acciones según sea necesario
        ]
        return context

  
class Crear_Seccion(LoginRequiredMixin, CreateView):
    permission_required = 'MacroProcesos.add_macroprocesos'
    model = Seccion
    form_class = Seccion_Form
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Retornar respuesta JSON si es AJAX
        else:
            return reverse_lazy('macroprocesos:Listar_Seccion')

    def form_valid(self, form):
        seccion = form.cleaned_data.get('Seccion')
        log_event(self.request.user, "info", f"Se creó la Sección: {seccion}")

        # Verificar si la solicitud es AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response_data = {'success': True, 'url': self.get_success_url()}
            return JsonResponse(response_data)

        return super().form_valid(form)  # Redirigir normalmente para solicitudes no AJAX

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Sección'
        context['entity'] = 'Sección'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Seccion')
        return context
class Editar_Seccion(LoginRequiredMixin, UpdateView):
    permission_required = 'MacroProcesos.change_macroprocesos'
    model = Seccion
    form_class = Seccion_Form
    template_name = 'shared/create.html'
    
    def get_success_url(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})  # Retornar respuesta JSON si es AJAX
        else:
            return reverse_lazy('macroprocesos:Listar_Seccion')
        
    def form_valid(self, form):
        seccion = form.cleaned_data.get('Seccion')
        log_event(self.request.user, "info", f"Se Edito la Seccion. {seccion}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Seccion'
        context['entity'] = 'Seccion'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Seccion')
        return context
    
class Eliminar_Seccion(LoginRequiredMixin, DeleteView):
    permission_required = 'MacroProcesos.delete_macroprocesos'
    model = Seccion
    template_name = 'shared/del.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            pass
        else:
            return reverse_lazy('macroprocesos:Listar_Seccion')

    def form_valid(self, form):
        seccion = self.get_object()
        log_event(self.request.user, "info", f"Se Elimino la Seccion. {seccion.Seccion}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['title'] = 'Eliminar Seccion'
        context['entity'] = 'Seccion'
        context['texto'] = f'Seguro de eliminar la seccion {self.object.Seccion}?'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Seccion')
        return context