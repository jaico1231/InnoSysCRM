from django.contrib.auth.models import Group
from django.http import JsonResponse
from shared.forms.group_form import GroupForm, GroupFormCreate
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

from shared.loggin import log_event

class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'auth.view_group'
    model = Group
    template_name = 'shared/list.html'
    context_object_name = 'groups'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Grupos'
        context['entity'] = 'Grupos'
        context['Btn_Add'] =[
            {
            'name':'add',
            'label':'Crear Grupo',
            'icon':'add',
            'url':'shared:groupcreate', 
            # 'modal':'Activar',
            }
        ]
        context['headers'] = [ 'NOMBRES DE GRUPOS']
        context['fields'] = ['name']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'shared:groupedit',
                # 'modal': 'Activar'
                },
                {
                    'name': 'delete',
                    'label': '',
                    'icon': 'delete',
                    'color': 'danger',
                    'color2': 'white',
                    'url': 'shared:groupdel',
                    'modal': '1'
                },
        ]
        return context

    def get_absolute_url(self):
        return reverse_lazy('shared:groupslist')
class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'auth.view_group'
    model = Group
    form_class = GroupFormCreate
    template_name = 'shared/grupos_create.html'
    success_message = 'Creado correctamente'
    success_url = reverse_lazy('shared:groupslist')

    def form_valid(self, form):
        group = form.save(commit=False)
        group.save()
        form.save_m2m()  # Para guardar los permisos many-to-many
        permissions = form.cleaned_data.get('permissions_from')
        if permissions:
            group.permissions.set(permissions)
        log_event(self.request.user, "info", f"Se creó el grupo: {form.cleaned_data['name']}")
        messages.success(self.request, self.success_message)
        return super().form_valid(form)  

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el grupo')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Grupo'
        context['entity'] = 'Grupos'
        context['list_url'] = 'shared:groupslist'
        context['action'] = 'add'
        return context
    
class GroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'auth.view_group'
    model = Group
    form_class = GroupForm
    template_name = 'shared/grupos.html'
    success_message = 'Actualizado correctamente'
    success_url = reverse_lazy('shared:groupslist')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        log_event(self.request.user, "info", f"Se actualizo el grupo: {form.cleaned_data['name']}")
      
        return super().form_valid(form)

    def form_invalid(self, form):
        # genera el error de validación de formulario
        print(form.errors)
        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Grupo'
        context['entity'] = 'Grupos'
        context['list_url'] = 'shared:groupslist'
        context['action'] = 'edit'
        return context


class GroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'auth.view_group'    
    model = Group
    template_name = 'shared/del.html'
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('shared:userlist')
    def form_valid(self, form):
        grupo = self.get_object()
        messages.success(self.request, 'Eliminado correctamente')
        log_event(self.request.user, "info", f"Se elimino el grupo: {grupo.name}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Grupo'
        context['entity'] = 'Grupos'
        context['texto'] = f'Seguro de eliminar el Grupo {self.object}?'
        context['list_url'] = 'shared:groupslist'
        return context