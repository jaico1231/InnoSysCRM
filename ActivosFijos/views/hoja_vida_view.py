
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ActivosFijos.models.hoja_vida_articulo import Hoja_Vida_Articulos
from ActivosFijos.forms import *

class Listar_Hoja_Vida_ArticulosView(ListView):
    model = Hoja_Vida_Articulos
    template_name = 'HojaVidaArticulos/Listar_Hoja_Vida_Articulos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Articulos'
        context['entity'] = 'Articulos'
        return context
class Crear_Hoja_Vida_ArticulosView(CreateView):
    form_class = Hoja_Vida_ArticulosForm
    template_name = 'HojaVidaArticulos/Crear_Hoja_Vida_Articulos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_Hoja_Vida_Articulos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Articulos'
        context['entity'] = 'Articulos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_Hoja_Vida_Articulos')
        return context
class Editar_Hoja_Vida_ArticulosView(UpdateView):
    model = Hoja_Vida_Articulos
    form_class = Hoja_Vida_ArticulosForm
    template_name = 'HojaVidaArticulos/Crear_Hoja_Vida_Articulos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_Hoja_Vida_Articulos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Articulos'
        context['entity'] = 'Articulos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_Hoja_Vida_Articulos')
        return context
    
class Borrar_Hoja_Vida_ArticulosView(DeleteView):
    model = Hoja_Vida_Articulos
    template_name = 'HojaVidaArticulos/Borrar_Hoja_Vida_Articulos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_Hoja_Vida_Articulos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Articulos'
        context['entity'] = 'Articulos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_Hoja_Vida_Articulos')
        return context