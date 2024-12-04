from shared.forms.MenuForms import MenuForm, MenuItemForm
from shared.loggin import log_event
from shared.models.menu import MenuItem, Menu
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import  JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

class ToggleMenuEstadoView(LoginRequiredMixin, UpdateView):
    model = Menu
    fields = ['estado']
    success_url = reverse_lazy('shared:menu')

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        menu = get_object_or_404(Menu, pk=kwargs['pk'])
        # Invertir el estado de 'activo' o 'estado'
        menu.estado = not menu.estado
        menu.save()
        x = Menu.objects.get(id=menu.id)
        log_event(request.user, 'menu', f'se cambio el estado del menu {menu.name} a {menu.estado}', )
        print(f'Nuevo estado de menu {menu.id}: {menu.estado}')  # Añadir un log para verificar el cambio
        return JsonResponse({'success': True, 'estado': menu.estado})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Activar Servicio'
        context['entity'] = 'Servicio'
        context['list_url'] = 'administrativo:servicioslist'
        return context

class ToggleMenuItelEstadoView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    fields = ['estado']
    success_url = reverse_lazy('shared:menuitems')

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        menu = get_object_or_404(MenuItem, pk=kwargs['pk'])
        # Invertir el estado de 'activo' o 'estado'
        menu.estado = not menu.estado
        menu.save()
        x = MenuItem.objects.get(id=menu.id)
        log_event(request.user, 'menu', f'se cambio el estado del menu {menu.name} a {menu.estado}', )
        print(f'Nuevo estado de menu {menu.id}: {menu.estado}')  # Añadir un log para verificar el cambio
        return JsonResponse({'success': True, 'estado': menu.estado})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Activar Servicio'
        context['entity'] = 'Servicio'
        context['list_url'] = 'administrativo:servicioslist'
        return context

class ListMenuView(ListView, PermissionRequiredMixin):
    permission_required = 'shared.view_menu'
    model=Menu
    template_name = 'shared/list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Menu'
        context['entity'] = 'shared'
        context['headers'] = ['NOMBRE', 'ICONO', 'ACTIVO']
        context['fields'] = ['name', 'icon']
        context['url_toggle'] = 'shared:togglemenu'
        context['actions'] = [
            {
                'name': 'edit',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'shared:editmenu',
                'modal': 'Activar'
            }
            ]
        context['cancel_url'] = reverse_lazy('shared:menu')
        return context

class MenuCreateView(CreateView, PermissionRequiredMixin):
    permission_required = 'shared.add_menu'
    model=Menu
    template_name = 'shared/form.html'
    form_class = MenuItem
    success_url = reverse_lazy('shared:menu')

    def form_valid(self, form):
        form.instance.group = self.request.user.groups.first()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Menu'
        context['entity'] = 'shared'
        context['action'] = 'add'
        return context

class MenuUpdateView(UpdateView, PermissionRequiredMixin):
    permission_required = 'shared.change_menu'
    model=Menu
    template_name = 'shared/create.html'
    form_class = MenuForm
    success_message = "Menu actualizado con exito"
        
    def get_success_url(self):
        if self.request.accepts('application/json/html'):
            return JsonResponse({'success': True, 'message': self.success_message})
        else:
            return reverse_lazy('shared:menu')
        
    def form_valid(self, form):
        menu=self.get_object()
        messages.success(self.request, self.success_message)
        log_event(self.request.user, "info", f"Se actualizo el menu. {menu}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Menu'
        context['entity'] = 'shared'
        context['action'] = 'edit'
        return context
    
class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Menu'
        context['entity'] = 'shared'
        context['headers'] = ['MENU', 'NOMBRE', 'URL', 'ICONO', 'ACTIVO']
        context['fields'] = ['menu', 'name', 'url_name', 'icon']
        context['url_toggle'] = 'shared:togglemenuitem'
        context['Btn_Add'] = [
            {
                'name': 'add',
                'label': 'Agregar',
                'icon': 'add',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'shared:menuitemscreate',
                'modal': 'Activar'
            }
        ]
        
        context['actions'] = [
            {
                'name': 'edit',
                'icon': 'edit',                
                'color': 'secondary',
                'color2': 'brown',
                'url': 'shared:editmenuitem',
                'modal': 'Activar'
            }
            ]
        context['cancel_url'] = reverse_lazy('shared:menu')
        
        return context

class MenuItemCreateView(CreateView, PermissionRequiredMixin):
    permission_required = 'shared.add_menuitem'
    model = MenuItem
    template_name = 'shared/create.html'
    form_class = MenuItemForm
    success_message = "Menu creado con exito"

    def get_success_url(self):
        if self.request.accepts('application/json/html'):
            return JsonResponse({'success': True, 'message': self.success_message})
        else:
            return reverse_lazy('shared:menuitemlist')
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        menu= form.cleaned_data.get('name')
        log_event(self.request.user, "info", f"Se creo el menu. {menu}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Menu Item'
        context['entity'] = 'shared'
        context['action'] = 'add'
        return context
      
class MenuItemUpdateView(UpdateView, PermissionRequiredMixin):
    permission_required = 'shared.change_menuitem'
    model = MenuItem
    template_name = 'shared/create.html'
    form_class = MenuItemForm
    success_message = "Menu actualizado con exito"

    def get_success_url(self):
        if self.request.accepts('application/json/html'):
            return JsonResponse({'success': True, 'message': self.success_message})
        else:
            return reverse_lazy('shared:menuitemlist')
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        menu= form.cleaned_data.get('name')
        log_event(self.request.user, "info", f"Se actualizo el menu. {menu}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Menu Item'
        context['entity'] = 'shared'
        context['action'] = 'edit'
        return context

