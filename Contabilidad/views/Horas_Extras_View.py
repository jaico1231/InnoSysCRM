from Contabilidad.forms.iniciales_form import HorasExtrasForm
from Contabilidad.models.conceptos import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from shared.loggin import log_event

class HorasExtrasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'Contabilidad.view_configuracionhorasextras'
    model = ConfiguracionHorasExtras
    template_name = 'shared/list.html'
    context_object_name = 'horas_extras'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Horas Extras'
        context['entity'] = 'Horas Extras'
        context['add_url'] = reverse_lazy('contabilidad:H_E_Create')
        context['headers'] = [ 'Nombre','Codigo', '% Decimal']
        context['fields'] = ['nombre','codigo', 'porcentaje']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'contabilidad:H_E_Update',
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'contabilidad:H_E_Delete',
                # 'modal': '1'
            }
        ]
        return context

class CreateHorasExtrasView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Contabilidad.add_configuracionhorasextras'
    model = ConfiguracionHorasExtras
    form_class = HorasExtrasForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('text/html/application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('contabilidad:H_E_List')

    def form_valid(self, form):
        extra=form.cleaned_data.get('porcentaje')
        log_event(self.request.user, 'info', f'Se agrego la hora extra {form.instance}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Horas Extras'
        context['entity'] = 'Horas Extras'
        context['action'] = 'add'
        return context
    
class UpdateHorasExtrasView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Contabilidad.change_configuracionhorasextras'
    model = ConfiguracionHorasExtras
    form_class = HorasExtrasForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('text/html/application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('contabilidad:H_E_List')
    def form_valid(self, form):
        log_event(self.request.user, 'info', f'Se actualizo la hora extra {form.instance}')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Horas Extras'
        context['entity'] = 'Horas Extras'
        context['action'] = 'edit'
        return context

class DeleteHorasExtrasView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Contabilidad.delete_configuracionhorasextras'
    model = ConfiguracionHorasExtras
    template_name = 'shared/del.html'
    
    def get_success_url(self):
        if self.request.accepts('text/html/application/json'):
            return JsonResponse({'success': True})
        else:
            return reverse_lazy('contabilidad:H_E_List')
        
    def form_valid(self, form):
        extra = self.get_object()
        log_event(self.request.user, 'info', f'Se elimino la hora extra {extra.nombre}')
        return super().form_valid(form)    
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Horas Extras'
        context['entity'] = 'Horas Extras'
        context['texto'] = f'¿Seguro de eliminar la hora extra {context["object"].nombre}?'
        return context