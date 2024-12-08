
from django.views.generic import ListView, CreateView
from ActivosFijos.models.inventario import Inventario

class InventarioView(ListView):
    model = Inventario
    template_name = 'Inventario/Listar_Inventario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Inventario'
        context['entity'] = 'Inventario'
        return context
    
class RegistrarMovimientoView(CreateView):
    model = Inventario
    fields = ['IdArticuloFK', 'Cantidad']
    template_name = 'Inventario/registrar_movimiento.html'
    success_url = 'ACTIVOS:Inventario'

    def form_valid(self, form):
        inventario = form.save(commit=False)
        if inventario.cantidad > 0:
            inventario.save()
        else:
            # Manejar la salida de inventario
            inventario.cantidad = -inventario.cantidad
            inventario.save()
        return super().form_valid(form)  