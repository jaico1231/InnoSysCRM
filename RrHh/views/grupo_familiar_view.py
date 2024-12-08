
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from RrHh.forms.grupo_familiar_form import Grupo_FamiliarForm
from RrHh.models.grupo_familiar import Grupo_Familiar
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
class Listar_Grupo_Familiar(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'RrHh.view_grupofamiliar'
    model = Grupo_Familiar
    template_name = 'HV/Listar_Grupo_Familiar.html'
    form_class = Grupo_FamiliarForm

    def get_queryset(self):
        print(self.kwargs['pk'])
        # return Grupo_Familiar.objects.filter(empleado_FK=self.kwargs['pk'])
        return Grupo_Familiar.objects.all()
 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Grupo Familiar'
        context['entity'] = 'Grupo Familiar'
        context['list_url'] = reverse_lazy('RrHh:Listar_Grupo_Familiar')
        return context
    
class Crear_Grupo_Familiar(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'RrHh.add_grupofamiliar'
    model = Grupo_Familiar
    form_class = Grupo_FamiliarForm
    template_name = 'HV/Crear_GrupoFamiliar.html'

    def get_success_url(self):
        return reverse_lazy('RrHh:Crear_GF')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("entramos a la vista" )
        context['title'] = 'Crear Grupo Familiar'
        context['entity'] = 'Grupo Familiar'
        context['GF_FORM'] = context['form']
        # context['list_url'] = reverse_lazy('RrHh:Listar_Grupo_Familiar')
        return context
    
    
class Editar_Grupo_Familiar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'RrHh.change_grupofamiliar'
    model = Grupo_Familiar
    form_class = Grupo_FamiliarForm
    template_name = 'HV/Crear_Grupo_Familiar.html'
    # success_url = reverse_lazy('RrHh:Listar_Grupo_Familiar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Grupo Familiar'
        context['entity'] = 'Grupo Familiar'
        context['list_url'] = reverse_lazy('RrHh:Listar_Grupo_Familiar')
        return context

class Borrar_Grupo_Familiar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'RrHh.delete_grupofamiliar'
    model = Grupo_Familiar
    template_name = 'HV/Borrar_Grupo_Familiar.html'
    # success_url = reverse_lazy('RrHh:Listar_Grupo_Familiar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Grupo Familiar'
        context['entity'] = 'Grupo Familiar'
        context['list_url'] = reverse_lazy('RrHh:Listar_Grupo_Familiar')
        return context
