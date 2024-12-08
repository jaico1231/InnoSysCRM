from django import forms
from django.http import JsonResponse
from django.urls import reverse_lazy
from Produccion.forms.FormicaForm import PrecioSuperficieForm, Precio_Superficie 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from shared.loggin import log_event


class Listar_Precios_Superficie(LoginRequiredMixin,  PermissionRequiredMixin,ListView):
    permission_required = 'Produccion.view_preciosuperficie'
    model = Precio_Superficie
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Precios Superficies'
        context['entity'] = 'Precios Superficies'
        context['Btn_Add'] = [
            {
                'url':'Produccion:Crear_Precios_Superficie',
                'modal': 'Activar',
                }   
                ]
        context['headers'] = ['SUPERFICIE', 'MEDIDA', 'CLIENTE FINAL CON TRANSPORTE', 'CLIENTE FINAL EN FABRICA', 'PRECIO DISTRIBUIDOR' ]
        context['fields'] = ['Formica_FK','Medida_FK','CFT','CFEF','PD']
        context['actions'] = [
            
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'Produccion:Editar_Precios_Superficie',
                'modal': '1'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'Produccion:Borrar_Precios_Superficie',
                'modal': '1'
            }
        ]
        return context

class Crear_Precio_Superficie(LoginRequiredMixin,  PermissionRequiredMixin,CreateView):
    permission_required = 'Produccion.add_preciosuperficie'
    model = Precio_Superficie
    template_name = 'shared/create.html'
    form_class = PrecioSuperficieForm
    success_message = "Precio Superficie Creada con Exito"

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True, 'message': self.success_message})
        return reverse_lazy('Produccion:Listar_Precios_Superficie')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user, 'info', f'Precio Superficie {form.instance} Creada con Exito')
        return response

    def form_invalid(self, form):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': False, 'errors': form.errors})
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Precio Superficie'
        context['entity'] = 'Precios Superficies'
        context['list_url'] = 'Produccion:Listar_Precios_Superficie'
        context['action'] = 'add'
        return context
class Editar_Precio_Superficie(LoginRequiredMixin,  PermissionRequiredMixin,UpdateView):
    permission_required = 'Produccion.change_preciosuperficie'
    model = Precio_Superficie
    template_name = 'shared/create.html'
    form_class = PrecioSuperficieForm

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('Produccion:Listar_Precios_Superficie')
        
    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user, 'info', f'Precio Superficie {form.instance} Creada con Exito')
        return response

    def form_invalid(self, form):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': False, 'errors': form.errors})
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Precio Superficie'
        context['entity'] = 'Precios Superficies'
        context['list_url'] = 'Produccion:Listar_Precios_Superficie'
        context['action'] = 'edit'
        return context

class Borrar_Precio_Superficie(LoginRequiredMixin,  PermissionRequiredMixin,DeleteView):
    permission_required = 'Produccion.delete_preciosuperficie'
    template_name = 'shared/del.html'
    model = Precio_Superficie

    def get_success_url(self):
        if self.request.headers.get('accept') == 'application/json':
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('Produccion:Listar_Precios_Superficie')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user, 'info', f'Precio Superficie {response.instance} Eliminada con Exito')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Precio Superficie'
        context['entity'] = 'Precios Superficies'
        context['list_url'] = 'Produccion:Listar_Precios_Superficie'
        return context