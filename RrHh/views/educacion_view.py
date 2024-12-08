from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from RrHh.forms import EducacionForm
from RrHh.models.educacion import Educacion
from django.contrib.auth.mixins import LoginRequiredMixin
class Crear_Educacion(LoginRequiredMixin, CreateView):
    form_class = EducacionForm
    template_name = 'HV/Crear_Educacion.html'
    # success_url = reverse_lazy('RrHh:Listar_HV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('Entramos en la vista de Crear Educación')
        context['title'] = 'Crear Educación'
        context['entity'] = 'Educación'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
class Editar_Educacion(LoginRequiredMixin, UpdateView):
    model = Educacion
    form_class = EducacionForm
    template_name = 'HV/Crear_Educacion.html'
    # success_url = reverse_lazy('RrHh:Listar_HV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Educación'
        context['entity'] = 'Educación'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
class Borrar_Educacion(LoginRequiredMixin, DeleteView):
    model = Educacion
    template_name = 'HV/Borrar_Educacion.html'
    # success_url = reverse_lazy('RrHh:Listar_HV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Educación'
        context['entity'] = 'Educación'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
