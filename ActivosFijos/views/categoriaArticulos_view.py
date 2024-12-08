from datetime import timedelta
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ActivosFijos.forms.categpriasArt_form import Categoria_Articulo_Form
from ActivosFijos.models.categoria_articulos import Categoria_Articulo

from shared.loggin import log_event

class Listar_Categoria_ArticulosView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'ActivosFijos.view_categoriaarticulo'
    model = Categoria_Articulo
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Grupo de Articulos'
        context['entity'] = 'Grupo de Articulos'
        context['Btn_Add'] = [
            {
                'url':'ACTIVOS:Crear_GRUPO_ART',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['CODIGO', 'DESCRIPCION', 'ESTADO', 'FECHA_CREACION']  # Encabezados de columnas
        context['fields'] = ['Id_GrupoArticulo', 'Descripcion', 'Estado', 'fecha_creacion'] 
        context['actions'] = [
            {
                'name': 'edit', 
                'label': '', 
                'icon': 'edit', 
                'color': 'secondary', 
                'color2': 'brown', 
                'url': 'ACTIVOS:Editar_GRUPOART',
                'modal': 'Activa'
            },
            {
                'name': 'delete', 
                'label': '', 
                'icon': 'delete', 
                'color': 'danger',
                'color2': 'white', 
                'url': 'ACTIVOS:Borrar_GRUPO_ART',
                'modal': 'Activa'
            },
        ]
        return context
    
class Crear_Categoria_ArticulosView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'ActivosFijos.add_categoriaarticulo'
    model = Categoria_Articulo
    form_class = Categoria_Articulo_Form
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_GRUPO_ART')

    def form_valid(self, form):
        G_Art = form.cleaned_data.get('Descripcion')
        log_event(self.request.user, 'info', f'Crea una categoria de articulos {G_Art}')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Categorias de Articulos'
        context['entity'] = 'Crear Grupo'
        context['list_url'] = 'ACTIVOS:Listar_GRUPO_ART'
        return context
    
class Editar_Categoria_ArticulosView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'ActivosFijos.change_categoriaarticulo'
    model = Categoria_Articulo
    form_class = Categoria_Articulo_Form
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_GRUPO_ART')

    def form_valid(self, form):
        G_Art = form.cleaned_data.get('Descripcion')
        log_event(self.request.user, 'info', f'Edita una categoria de articulos {G_Art}')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categorias de Articulos'
        context['entity'] = 'Categorias de Articulos'
        context['list_url'] = 'ACTIVOS:Listar_GRUPO_ART'
        return context

class Eliminar_Categoria_ArticulosView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'ActivosFijos.delete_categoriaarticulo'
    model = Categoria_Articulo
    template_name = 'shared/del.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_GRUPO_ART')
    
    def form_valid(self, form):
        G_Art = self.get_object()
        log_event(self.request.user, 'info', f'Elimina una categoria de articulos {G_Art}')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Categorias de Articulos'
        context['entity'] = 'Categorias de Articulos'
        context['list_url'] = 'ACTIVOS:Listar_GRUPO_ART'
        context['texto'] = f'¿Desea eliminar el grupo de articulos {self.object.Descripcion}?'
        return context