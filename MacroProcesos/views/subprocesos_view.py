from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import  HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from shared.loggin import log_event
from MacroProcesos.models.macroprocesos import Subprocesos
from MacroProcesos.forms.macro_procesos_form import Subproceso_Form


class Listar_Subprocesos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'MacroProcesos.view_subprocesos'
    model = Subprocesos
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super(Listar_Subprocesos, self).get_context_data(**kwargs)
        context['title'] = 'Listar Subprocesos'
        context['entity'] = 'Subprocesos'
        context['Btn_Add'] = [
            {
                'name':'add',
                'label':'Crear Subprocesos',
                'icon':'add',
                'url':'macroprocesos:Crear_Subprocesos',
                'modal': 'Activar',
        }
        ]
        context['headers'] = ['IDENTIFICADOR', 'SUBPROCESO', 'PROCESO']  # Encabezados de columnas
        context['fields'] = ['IdSubProceso', 'SubProceso', 'proceso_FK']  # Campos del modelo
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'macroprocesos:Editar_Subprocesos',
                'modal': 'Activar',
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'macroprocesos:Eliminar_Subprocesos',
                'modal': 'Activar',
            
        }]
        return context


class Crear_Subprocesos(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'MacroProcesos.add_subprocesos'
    model = Subprocesos
    form_class = Subproceso_Form
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('macroprocesos:Listar_Subprocesos')

    def form_valid(self, form):
        subproceso = form.save()
        messages.success(self.request, 'Subproceso creado con exito!')
        log_event(self.request.user, 'info', f'Subproceso {subproceso} creado con Exito')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(Crear_Subprocesos, self).get_context_data(**kwargs)
        context['title'] = 'Crear Subprocesos'
        context['entity'] = 'Subprocesos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Subprocesos')
        context['cancel_url'] = reverse_lazy('macroprocesos:Listar_Subprocesos')
        context['action'] = 'add'
        return context


class Editar_Subprocesos(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'MacroProcesos.change_subprocesos'
    model = Subprocesos
    form_class = Subproceso_Form
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('macroprocesos:Listar_Subprocesos')

    def form_valid(self, form):
        subproceso = form.save()
        messages.success(self.request, 'Subproceso actualizado con exito!')
        log_event(self.request.user, 'info', f'Subproceso {subproceso} actualizado con Exito')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Editar_Subprocesos, self).get_context_data(**kwargs)
        context['title'] = 'Editar Subprocesos'
        context['entity'] = 'Subprocesos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Subprocesos')
        context['cancel_url'] = reverse_lazy('macroprocesos:Listar_Subprocesos')
        context['action'] = 'edit'
        return context
    

class Eliminar_Subprocesos(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'MacroProcesos.delete_subprocesos'
    model = Subprocesos
    template_name = 'shared/delete.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('macroprocesos:Listar_Subprocesos')

    def get_context_data(self, **kwargs):
        context = super(Eliminar_Subprocesos, self).get_context_data(**kwargs)
        context['title'] = 'Eliminar Subprocesos'
        context['entity'] = 'Subprocesos'
        context['texto'] = f'Seguro de eliminar el subproceso {self.object.SubProceso}?'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_Subprocesos')
        return context
