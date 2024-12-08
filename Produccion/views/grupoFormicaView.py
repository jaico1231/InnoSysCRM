from django import forms
from django.http import JsonResponse
from django.urls import reverse_lazy
from Produccion.forms.FormicaForm import Grupo_Formica, GrupoFormicaForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from shared.loggin import log_event


class Listar_Grupos_Formicas(LoginRequiredMixin,  PermissionRequiredMixin,ListView):
    permission_required = 'Produccion.view_grupoformica'
    model = Grupo_Formica
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Grupo Formicas'
        context['entity'] = 'Formicas'
        context['Btn_Add'] = [   
            {
                'url':'Produccion:Crear_Grupos_Formicas',
                'modal': 'Activar',
                }   
                ]   
        context['headers'] = ['GRUPO']
        context['fields'] = ['grupo']
        context['actions'] = [
            
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'Produccion:Editar_Grupos_Formicas',
                'modal': '1'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'Produccion:Borrar_Grupos_Formicas',
                'modal': '1'
            }
        ]
        return context

class Crear_GrupoFormica(LoginRequiredMixin,  PermissionRequiredMixin,CreateView):
    permission_required = 'Produccion.add_grupoformica'
    template_name = 'shared/create.html'
    form_class = GrupoFormicaForm
    success_message = "Formica Creada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        return reverse_lazy('Produccion:Listar_Grupos_Formicas')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user,'info', f'Grupo Formica {form.instance} Creada con Exito')
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Formica'
        context['entity'] = 'Formica'
        context['list_url'] = 'Produccion:Listar_Grupos_Formicas'
        return context
    
class Editar_GrupoFormica(LoginRequiredMixin,  PermissionRequiredMixin,UpdateView):
    permission_required = 'Produccion.change_grupoformica'
    template_name = 'shared/create.html'
    form_class = GrupoFormicaForm
    model = Grupo_Formica
    success_message = "Formica Creada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('Produccion:Listar_Grupos_Formicas')
        
    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user,'info', f'Grupo Formica {form.instance} Editada con Exito')
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Formica'
        context['entity'] = 'Formica'
        context['list_url'] = 'Produccion:Listar_Grupos_Formicas'
        return context
    
class Borrar_GrupoFormica(LoginRequiredMixin,  PermissionRequiredMixin,DeleteView):
    permission_required = 'Produccion.delete_grupoformica'
    template_name = 'shared/del.html'
    model = Grupo_Formica
    success_message = "Formica Eliminada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('Produccion:Listar_Grupos_Formicas')
    def form_valid(self, form):
        self.object = self.get_object()
        grupofomica = Grupo_Formica.objects.get(id=self.object.id)
        log_event(self.request.user,'info', f'Grupo Formica {grupofomica} Eliminada con Exito')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Formica'
        context['texto'] = f'Seguro de eliminar el grupo {context["object"].grupo}'
        context['entity'] = 'Formica'
        context['list_url'] = 'Produccion:Listar_Grupos_Formicas'
        return context