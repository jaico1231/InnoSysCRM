from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ActivosFijos.models.presupuestos import Presupuestos
from ActivosFijos.forms import PresupuestoForm
class PresupuestoView(ListView):
    model = Presupuestos
    template_name = 'Presupuesto/PresupuestoList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Presupuestos'
        context['entity'] = 'Presupuestos'
        # context['form'] = HojaVidaForm()
        return context
class Crear_PresupuestoView(CreateView):
    form_class = PresupuestoForm
    template_name = 'base_ActivosFijos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_PRESUPUESTO')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_PRESUPUESTO')
        return context

class Editar_PresupuestoView(UpdateView):
    model = Presupuestos
    form_class = PresupuestoForm
    template_name = 'base_ActivosFijos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_PRESUPUESTO')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Presupuesto'
        context['element'] = 'Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_PRESUPUESTO')
        context['cancel_url']="../../activosfijos/presupuesto/"
        return context

class Borrar_PresupuestoView(DeleteView):
    model = Presupuestos
    template_name = 'Presupuesto/Borrar_Presupuesto.html'
    success_url = reverse_lazy('ACTIVOS:Listar_PRESUPUESTO')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Presupuesto'
        context['element'] = 'Presupuesto'
        context['entity'] = 'Presupuestos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_PRESUPUESTO')
        return context