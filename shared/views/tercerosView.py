from django.views.generic import ListView, CreateView, UpdateView, DeleteView,FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import  JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from shared.views.updateView import CargarCSVView
from shared.loggin import log_event
from shared.forms.tercerosForm import TercerosForm
from shared.models.terceros import Terceros

import csv
from django.shortcuts import render, redirect

class CargarTercerosCSVView(CargarCSVView):
    model_name = 'Terceros'
    success_message = "Terceros cargados con éxito"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_label'] = 'shared'
        context['model_name'] = self.model_name
        context['cancel_url'] = reverse_lazy('shared:terceroslist')
        return context
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
class TercerosListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'shared.view_terceros'
    model = Terceros
    template_name = 'shared/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de terceros'
        context['entity'] = 'Terceros'        
        context['Btn_Add'] = [
            {   
                'name': 'add',
                'label': 'Crear Tercero',
                'url':'shared:terceroscreate',
                'modal': 'Activar',
            },
            {
                'name': 'csv',
                'label': 'Cargar desde CSV',
                'url':'shared:cargar_terceros_csv',
                
            }
                ]
        context['headers'] = [ 'ID','NOMBRE','APELLIDO', 'TELEFONO', 'CORREO', 'CIUDAD', 'ASESOR']
        context['fields'] = ['NumeroIdentificacion', 'Nombre', 'Apellido', 'TelefonoMovil', 'Email', 'municipio_FK', 'asesor']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'white',
                'url': 'shared:tercerosedit',
                'modal': 'Activar'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'shared:tercerosdel',
                'modal': 'Activar'
            },
        ]
        return context

    
class TercerosCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shared.add_terceros'
    model = Terceros
    template_name = 'shared/create.html'
    form_class = TercerosForm
    success_message = "Tercero creado con éxito"

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True, 'message': self.success_message})
        else:
            return reverse_lazy('shared:terceros')

    def form_valid(self, form):
        print('entraste en form valid')
        messages.success(self.request, self.success_message)
        tercero = form.cleaned_data.get('Nombre')
        log_event(self.request.user, "info", f"Se creó el Tercero: {tercero}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Tercero'
        context['entity'] = 'Terceros'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('shared:terceros')
        return context

class TerceroUpdateView( LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shared.change_terceros'
    template_name = 'shared/create.html'
    form_class = TercerosForm
    model = Terceros
    success_message = "Tercero actualizado con exito"

    def get_success_url(self) -> str:
        if self.request.accepts('application/json/html'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('shared:terceros')

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        tercero = form.cleaned_data.get('Nombre')
        log_event(self.request.user, "info", f"Se Actualizo el Tercero. {tercero}")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Tercero'
        context['entity'] = 'Terceros'
        context['action'] = 'edit'
        return context

class TerceroDeleteView( LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'shared.delete_terceros'
    model = Terceros
    template_name = 'shared/del.html'

    def get_success_url(self) -> str:
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('shared:terceros')

    def form_valid(self, form):
        # messages.success(self.request.user, "Tercero eliminado con exito")
        tercero = self.get_object()
        log_event(self.request.user, "info", f"Se Elimino el Tercero. {tercero}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tercero'
        context['entity'] = 'Terceros'
        context['cancel_url'] = reverse_lazy('shared:terceros')
        context['texto'] = f'Seguro de eliminar el Tercero {self.object.Nombre}?'
        return context