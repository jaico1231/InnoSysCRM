from django import forms
from django.http import JsonResponse
from django.urls import reverse_lazy
from Produccion.forms.FormicaForm import FormicaForm, Formica
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from shared.loggin import log_event

class Listar_Formicas(LoginRequiredMixin,  PermissionRequiredMixin,ListView):
    permission_required = 'Produccion.view_formica'
    model = Formica
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Formicas'
        context['entity'] = 'Formicas'
        context['Btn_Add'] = [
            {
                'url':'Produccion:Crear_Formica',
                'modal': 'Activar',
                }   
                ]
        context['headers'] = ['FORMICA', 'GRUPO' ]
        context['fields'] = ['descripcion','grupo']
        context['actions'] = [
            
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'Produccion:Editar_Formica',
                'modal': '1'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'Produccion:Borrar_Formica',
                'modal': '1'
            }
        ]
        return context
    
class Crear_FormicaView(LoginRequiredMixin,  PermissionRequiredMixin,CreateView):
    permission_required = 'Produccion.add_formica'
    model = Formica
    form_class = FormicaForm
    template_name = 'shared/create.html'
    success_message = "Formica Creada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        return reverse_lazy('Produccion:Listar_Formica')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user, 'info', f'Se agrego correctamente la Formica. {form.instance}')
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Formica'
        context['entity'] = 'Formicas'
        context['list_url'] = reverse_lazy('Produccion:Listar_Formica')
        return context
    
class Editar_Formica(LoginRequiredMixin,  PermissionRequiredMixin,UpdateView):
    permission_required = 'Produccion.change_formica'
    model = Formica
    form_class = FormicaForm
    template_name = 'shared/create.html'
    success_message = "Formica Editada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('Produccion:Listar_Formica')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user, 'info', f'Se actualizo correctamente la Formica. {form.instance}')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Formica'
        context['entity'] = 'Formicas'
        context['list_url'] = reverse_lazy('Produccion:Listar_Formica')
        return context
    
class Borrar_Formica(LoginRequiredMixin,  PermissionRequiredMixin,DeleteView):
    permission_required = 'Produccion.delete_formica'
    model = Formica
    template_name = 'shared/del.html'
    success_message = "Formica Eliminada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('Produccion:Listar_Formica')

    def form_valid(self, form):
        datos = self.get_object()
        fomicaname = Formica.objects.get(id=datos.id)
        log_event(self.request.user, 'info', f'Se elimino correctamente la Formica {fomicaname}.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Formica'
        context['entity'] = 'Formicas'
        context['texto'] = f'¿Desea borrar la Formica {self.object}?'
        context['list_url'] = reverse_lazy('Produccion:Listar_Formica')
        return context