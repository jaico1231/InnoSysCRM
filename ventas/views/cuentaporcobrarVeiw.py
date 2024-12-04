from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,FormView
from django.contrib import messages
from configuracion.models.servicios import Medicos
from shared.forms.CxCForm import CuentaxCobrarForm
from shared.loggin import log_event
from ventas.models.ventas import CuentaPorCobrar, Venta

class CxCListView(ListView):
    model = CuentaPorCobrar
    template_name = 'shared/list.html'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # mostrar solo cuentas por cobrar con saldo pendiente
        context['object_list'] = CuentaPorCobrar.objects.filter(saldo_pendiente__gt=0)
        context['title'] = 'Cuentas por Cobrar'
        context['list_url'] = reverse_lazy('cuentaporcobrar')
        context['entity'] = 'Cuentas por Cobrar'
        context['Btn_Add'] = [
            {
                'name': 'add',
                'label': 'Crear Cuenta por Cobrar',
                'url': 'ventas:cxc_Create',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['FACTURA', 'MEDICO', 'FECHA DE VENCIMIENTO', 'SALDO PENDIENTE', 'TOTAL COBRADO']
        context['fields'] = ['venta', 'medico', 'fecha_vencimiento', 'saldo_pendiente', 'total_cobrado']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'white',
                'url': 'ventas:cxc_Update',
                'modal': 'Activar'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'ventas:cxc_Del',
                'modal': 'Activar'
            }
        ]
        return context
    
class CxCCreateView(CreateView):
    model = CuentaPorCobrar
    template_name = 'shared/create.html'
    form_class = CuentaxCobrarForm
    
    def get_success_url(self):
        return reverse_lazy('cxc_list')

    def form_valid(self, form):
        # Obtener la venta y el médico utilizando los valores de la URL
        venta = form.cleaned_data['venta']
        medico = venta.medico
              
        # Calcular la fecha de vencimiento, añadiendo 30 días a la fecha de la venta
        if hasattr(venta, 'fecha'):
            fecha_vencimiento = venta.fecha + timedelta(days=30)
        else:
            # Si el campo 'fecha' no existe o no está presente, manejar el error
            messages.error(self.request, 'La venta no tiene una fecha válida.')
            return self.form_invalid(form)

        # Asignar los valores correspondientes al formulario
        form.instance.venta = venta
        form.instance.medico = medico
        form.instance.fecha_vencimiento = fecha_vencimiento
        form.instance.saldo_pendiente = venta.total

        # Guardar la instancia del formulario
        form.save()

        # Mostrar mensaje de éxito
        messages.success(self.request, 'Cuenta por Cobrar creada con éxito')
        
        # Registro del evento (asegúrate de que log_event esté correctamente definido)
        log_event(self.request.user, 'info', f'Se agregó la Cuenta por Cobrar. {form.instance.venta}')
        
        # Finalizar y continuar con la lógica predeterminada
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cuentas por Cobrar'
        context['list_url'] = reverse_lazy('ventas:cxc_list')
        context['entity'] = 'Cuentas por Cobrar'
        context['action'] = 'add'
        return context

class CxCUpdateView(UpdateView):
    model = CuentaPorCobrar
    template_name = 'shared/create.html'
    form_class = CuentaxCobrarForm
    
    def get_success_url(self):
        return reverse_lazy('cxc_list')

    def form_valid(self, form):
        # Obtener la venta y el médico utilizando los valores de la URL
        venta = form.cleaned_data['venta']
        medico = venta.medico
              
        # Calcular la fecha de vencimiento, añadiendo 30 días a la fecha de la venta
        if hasattr(venta, 'fecha'):
            fecha_vencimiento = venta.fecha + timedelta(days=30)
        else:
            # Si el campo 'fecha' no existe o no está presente, manejar el error
            messages.error(self.request, 'La venta no tiene una fecha válida.')
            return self.form_invalid(form)

        # Asignar los valores correspondientes al formulario
        form.instance.venta = venta
        form.instance.medico = medico
        form.instance.fecha_vencimiento = fecha_vencimiento
        form.instance.saldo_pendiente = venta.total

        # Guardar la instancia del formulario
        form.save()

        # Guardar la instancia del formulario
        form.save()
        messages.success(self.request, 'Cuenta por Cobrar actualizada con exito')
        log_event(self.request.user, 'info', f'Se actualizo la Cuenta por Cobrar. {form.instance.venta}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cuentas por Cobrar'
        context['list_url'] = reverse_lazy('cuentaporcobrar')
        context['entity'] = 'Cuentas por Cobrar'
        context['action'] = 'edit'
        return context

class CxCDeleteView(DeleteView):
    model = CuentaPorCobrar
    template_name = 'shared/delete.html'
    success_url = reverse_lazy('cuentaporcobrar')

    def get_success_url(self):
        return reverse_lazy('cuentaporcobrar')

    def form_valid(self, form):
        messages.success(self.request, 'Cuenta por Cobrar eliminada con exito')
        log_event(self.request.user, 'info', f'Se elimino la Cuenta por Cobrar. {form.instance.venta}')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cuentas por Cobrar'
        context['list_url'] = reverse_lazy('cuentaporcobrar')
        context['entity'] = 'Cuentas por Cobrar'
        context['action'] = 'delete'
        return context