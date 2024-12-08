
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from ActivosFijos.models.orden_servicio import OrdenServicio
from ActivosFijos.forms import *

class Listar_OrdenesServicioView(ListView):
    model = OrdenServicio
    template_name = 'OrdenServicio/Listar_OrdenesServicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Ordenes de Servicio'
        context['entity'] = 'Ordenes de Servicio'
        return context

class Crear_OrdenesServicioView(CreateView):
    form_class = OrdenServicioForm
    template_name = 'OrdenServicio/Crear_OrdenesServicio.html'
    success_url = reverse_lazy('ACTIVOS:Listar_OS')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Ordenes de Servicio'
        context['entity'] = 'Ordenes de Servicio'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_OS')
        return context
    
class Detail_OrdenesServicioView(TemplateView):
    model = OrdenServicio
    template_name = 'OrdenServicio/Detalle_OrdenesServicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Orden de Servicio'
        context['entity'] = 'Ordenes de Servicio'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_OS')
class Editar_OrdenesServicioView(UpdateView):
    model = OrdenServicio
    form_class = OrdenServicioForm
    template_name = 'base_ActivosFijos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_OS')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Ordenes de Servicio'
        context['entity'] = 'Ordenes de Servicio'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_OS')
        return context
class Borrar_OrdenesServicioView(DeleteView):
    model = OrdenServicio
    template_name = 'OrdenServicio/Borrar_OrdenesServicio.html'
    success_url = reverse_lazy('ACTIVOS:Listar_OS')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Ordenes de Servicio'
        context['entity'] = 'Ordenes de Servicio'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_OS')
        return context