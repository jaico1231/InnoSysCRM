from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,FormView
from shared.forms.userForm import RenewPasswordForm, UserForm, UpdateUserForm, ChangePasswordForm
from shared.loggin import log_event
from shared.models.user import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


class UserListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    permission_required = 'shared.view_user'
    model = User
    template_name = 'shared/list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de usuarios'
        context['entity'] = 'Usuario'
        context['Btn_Add'] = [
            {
                'name': 'add',
                'label': 'Crear usuario',
                'icon': 'add',
                'url': 'shared:usercreate',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['NOMBRE DE USUARIO', 'NOMBRE', 'APELLIDO', 'CORREO', 'CEDULA']
        context['fields'] = ['username', 'first_name', 'last_name', 'email', 'NumeroIdentificacion']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'shared:useredit',
                'modal': 'Activar'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'shared:userdel',
                'modal': 'Activar'
            },
            {
                'name': 'password',
                'label': '',
                'icon': 'lock',
                'color': 'link',
                'color2': 'green',
                'url': 'shared:changepassword',
                'modal': 'Activar'
            }
        ]
        return context
    def get_absolute_url(self):
        return reverse_lazy('shared:userlist')

class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = 'shared.add_user'
    template_name = 'shared/create.html'
    form_class = UserForm
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('shared:userlist')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Encriptar el password
        user.save()
        #si el usuarion no se crea con exito, genere un mensaje de error
        if not user:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        messages.success(self.request, 'Usuario creado con exito')
        log_event(self.request.user, "info", f"Se Creó el usuario. {user.username}")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear usuario'
        context['entity'] = 'Usuario'
        context['list_url'] = reverse_lazy('shared:userlist')
        context['cancel_url'] = reverse_lazy('shared:userlist')
        context['action'] = 'add'          
        return context
   
class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shared.change_user'
    model = User
    form_class = UpdateUserForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        return reverse_lazy('shared:userlist')

    def form_valid(self, form):
        usuario = self.get_object()
        log_event(self.request.user, "info", f"Se actualizó el usuario: {usuario.username}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Editar usuario',
            'entity': 'Usuario',
            'list_url': reverse_lazy('shared:userlist'),
            'cancel_url': reverse_lazy('shared:userlist'),
        })
        return context

class UserDelView(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = 'shared.delete_user'
    model = User
    template_name = 'shared/del.html'
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('shared:userlist')

    def form_valid(self, form):
        user = self.get_object()
        log_event(self.request.user, "info", f"Se elimino el usuario. {user.username}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar usuario'
        context['entity'] = 'Usuario'
        context['texto'] = f'Seguro de eliminar el usuario {self.object.username}?'
        context['list_url'] = reverse_lazy('shared:userlist')
        return context

class PasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin,FormView):
    permission_required = 'shared.change_user'
    # form_class = PasswordChangeForm
    form_class = RenewPasswordForm
    template_name = 'Usuario/change_password.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('shared:userlist')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important, to update the session with the new password
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambia tu contraseña'
        context['entity'] = 'Usuario'
        context['list_url'] = self.success_url
        context['cancel_url'] = reverse_lazy('shared:index')
        return context
    
class RenewPasswordView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shared.change_user'
    model = User
    form_class = RenewPasswordForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('shared:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Encriptar el password
        user.save()
        usuario = self.get_object()
        log_event(self.request.user, "info", f"Se actualizo la password del usuario {usuario.username}.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambia tu contraseña'
        context['entity'] = 'Usuario'
        context['list_url'] = reverse_lazy('shared:login')
        context['cancel_url'] = reverse_lazy('shared:login')
        return context