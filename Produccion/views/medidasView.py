from django import forms
from django.http import JsonResponse
from django.urls import reverse_lazy
from Produccion.forms.FormicaForm import MedidasForm, Medidas
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from shared.loggin import log_event

class Listar_Medidas(LoginRequiredMixin,  PermissionRequiredMixin,ListView):
    permission_required = 'Produccion.view_medidas'
    model = Medidas
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Medidas'
        context['entity'] = 'Medidas'
        context['Btn_Add'] = [
            {
                'url':'Produccion:Crear_Medida',
                'modal': 'Activar',
                }   
                ]
        context['headers'] = ['MEDIDA', 'DESCRIPCION' ]
        context['fields'] = ['medida','Descripcion']
        context['actions'] = [
            
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'Produccion:Editar_Medida',
                'modal': '1',
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'Produccion:Borrar_Medida',
                'modal': '1'
            }
        ]
        return context

class Crear_Medida(LoginRequiredMixin,  PermissionRequiredMixin,CreateView):
    permission_required = 'Produccion.add_medidas'
    template_name = 'shared/create.html'
    model = Medidas
    form_class = MedidasForm
    success_message = "Medida Creada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        return reverse_lazy('Produccion:Listar_Medidas')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user,'info', f'Se agrego correctamente la Medida {form.instance}.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Medida'
        context['entity'] = 'Medidas'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('Produccion:Listar_Medidas')
        return context
    
class Editar_Medida(LoginRequiredMixin,  PermissionRequiredMixin,UpdateView):
    permission_required = 'Produccion.change_medidas'
    model = Medidas
    template_name = 'shared/create.html'
    form_class = MedidasForm
    success_message = "Medida Editada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        return reverse_lazy('Produccion:Listar_Medidas')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user,'info', f'Se editó correctamente la Medida {form.instance}.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Medida'
        context['entity'] = 'Medidas'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('Produccion:Listar_Medidas')
        return context
    
class Borrar_Medida(LoginRequiredMixin,  PermissionRequiredMixin,DeleteView):
    permission_required = 'Produccion.delete_medidas'
    model = Medidas
    template_name = 'shared/del.html'
    success_message = "Medida Eliminada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        return reverse_lazy('Produccion:Listar_Medidas')

    def form_valid(self, form):
        datos = self.get_object()
        Medidas.objects.get(pk=datos.pk)
        log_event(self.request.user,'info', f'Se elimino correctamente la Medida. {datos}.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Medida'
        context['entity'] = 'Medidas'
        context['texto'] = f'¿Estas seguro de eliminar la Medida {self.object}?'
        context['list_url'] = reverse_lazy('Produccion:Listar_Medidas')
        return context
        