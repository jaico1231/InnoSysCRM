from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from RrHh.forms.experiencia_laboral_form import ExperienciaForm
from django.contrib.auth.mixins import LoginRequiredMixin

class Crear_Experiencia_Laboral(LoginRequiredMixin, CreateView):
    form_class = ExperienciaForm
    template_name = 'HV/Crear_Experiencia_Laboral.html'
    # success_url = reverse_lazy('RrHh:Listar_HV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Experiencia Laboral'
        context['entity'] = 'Experiencia Laboral'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
    
class Editar_Experiencia_Laboral(LoginRequiredMixin, UpdateView):
    # model = Experiencia_Laboral
    form_class = ExperienciaForm
    template_name = 'HV/Crear_Experiencia_Laboral.html'
    # success_url = reverse_lazy('RrHh:Listar_HV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Experiencia Laboral'
        context['entity'] = 'Experiencia Laboral'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        return context

class Borrar_Experiencia_Laboral(LoginRequiredMixin, DeleteView):
    # model = ExperienciaForm
    template_name = 'HV/Borrar_Experiencia_Laboral.html'
    # success_url = reverse_lazy('RrHh:Listar_HV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Experiencia Laboral'
        context['entity'] = 'Experiencia Laboral'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
    