from django.http import HttpResponse
from django.urls import reverse_lazy
# from shared.forms.empresa_form import FormularioEmpresa
# from shared.models.datos_empresa import Empresa
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from shared.forms.DatosInicialesForm import DatosInicialesForm
from shared.models.datos_empresa import DatosIniciales
# ]from shared.loggin import log_event
class DatosInicialesView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = ['shared.add_empresa']
    model = DatosIniciales
    template_name = 'shared/create_no_modal.html'
    form_class = DatosInicialesForm
    
    # def some_view(request):
    #     # Your view logic here
    #     log_event(request.user, "info", "Se crearon los datos iniciales.")
    #     return HttpResponse("Event logged")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Datos Iniciales'
        context['entity'] = 'Datos Iniciales'        
        context['action'] = 'add'
        return context

class DatosInicialesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ['shared.change_empresa']
    model = DatosIniciales
    template_name = 'shared/create_no_modal.html'
    form_class = DatosInicialesForm
    success_url = reverse_lazy('shared:index')

    def get_object(self, queryset=None):
        """Override to always return the object with pk=1."""
        return self.model.objects.get(pk=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Datos Iniciales'
        context['entity'] = 'Datos Iniciales'
        context['list_url'] = reverse_lazy('shared:index')
        context['cancel_url'] = reverse_lazy('shared:index')
        context['action'] = 'edit'
        return context

    def get_absolute_url(self):
        return reverse_lazy('shared:inicialesUpdate')    
