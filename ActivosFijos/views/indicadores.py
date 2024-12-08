from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from ActivosFijos.forms.cronograma_form import CronogramaMantenimientoForm
from ActivosFijos.models.articulos import Articulo
from ActivosFijos.models.cronograma import  CronogramaMantenimiento, BitacoraMantenimiento
from django.views.generic.edit import *

class IndicadoresMantenimientoView(TemplateView):
    template_name = 'Cronograma/cronograma.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí puedes calcular los indicadores
        context['total_activos'] = Articulo.objects.count()
        context['mantenimientos_realizados'] = BitacoraMantenimiento.objects.count()
        context['mantenimientos_programados'] = CronogramaMantenimiento.objects.count()
        # Otros indicadores personalizados
        return context

class CargarDatosMantenimientoTerceroView(CreateView):
    model = CronogramaMantenimiento
    form_class = CronogramaMantenimientoForm
    success_url = reverse_lazy('ACTIVOS:Cr_Ma')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cargar Mantenimiento'
        context['entity'] = 'Articulos'
        context['list_url'] = reverse_lazy('ACTIVOS:Cr_Ma')
        return context