from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ActivosFijos.models.areas_trabajo import Areas_Trabajo
from ActivosFijos.forms import Areas_TrabajoForm

class Area_TrabajoView(ListView):
    model = Areas_Trabajo
    template_name = 'Area_Trabajo/Area_TrabajoList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Areas de Trabajo'
        context['entity'] = 'Areas de Trabajo'
        return context

class Crear_Area_TrabajoView(CreateView):
    form_class = Areas_TrabajoForm
    template_name = 'base_ActivosFijos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_AT')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Area de Trabajo'
        context['entity'] = 'Area de Trabajo'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_AT')

        return context
class Editar_Area_TrabajoView(UpdateView):
    model = Areas_Trabajo
    form_class = Areas_TrabajoForm
    template_name = 'base_ActivosFijos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_AT')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Area de Trabajo'
        context['entity'] = 'Area de Trabajo'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_AT')
        return context
class Borrar_Area_TrabajoView(DeleteView):
    model = Areas_Trabajo
    template_name = 'Area_Trabajo/Borrar_Area_Trabajo.html'
    success_url = reverse_lazy('ACTIVOS:Listar_AT')
    # traeme los datos del area de trabajo
    def get_object(self, queryset=None):
        obj = super().get_object()
        self.element = obj.Descripcion
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Area de Trabajo'
        context['entity'] = 'Area de Trabajo'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_AT')
        context['object'] = self.get_object()
        return context