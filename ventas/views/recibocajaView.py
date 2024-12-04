from datetime import date
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ventas.forms.recibocajaForm import ReciboCaja2Form, ReciboCajaForm

from ventas.models.ventas import CuentaPorCobrar, ReciboCaja, Venta
from django.db import transaction

# Lista de recibos de caja
class ReciboCajaListView(ListView):
    model = ReciboCaja
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Recibos de Caja'
        context['entity'] = 'Recibos de Caja'
        context['Btn_Add'] = [{
            'named': 'add_caja',
            'label': 'Registrar Caja',
            'url': 'ventas:RC_create2',
            # 'modal': 'Activar',
        }]
        context['headers'] = ['N°', 'FECHA', 'TIPO DE PAGO', 'TOTAL']
        context['fields'] = ['id', 'fecha', 'metodo_pago', 'total']
        context['actions'] = [
            {
                'name': 'edit',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'white',
                'url': 'ventas:RC_Update',
                'modal': 'Activar',
            },
            {
                'name': 'delete',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'ventas:RC_Del',
                'modal': 'Activar',
            },
        ]
        return context
    
class ReciboCajaCreateView(CreateView):
    model = ReciboCaja
    template_name = 'ventas/create2.html'
    form_class = ReciboCajaForm

    def get_success_url(self):
        
        # Comprobar si la solicitud es AJAX
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse('ventas:recibo_caja_list')  # Cambia esto por el nombre correcto de la URL
        
    @transaction.atomic
    def form_valid(self, form):
        # Asociar el pago a la venta correcta
        venta = get_object_or_404(Venta, id=self.kwargs['venta_id'])
        form.instance.venta = venta
        recibo_caja = form.save(commit=False)
        cuenta_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
        monto_pagado = form.cleaned_data['total']
        
        # Registrar el pago en la cuenta por cobrar
        cuenta_por_cobrar.registrar_pago(recibo_caja, monto_pagado)
        recibo_caja.save()

        # Guardar el pago parcial
        response = super().form_valid(form)
        # Mensaje según el estado de la cuenta por cobrar
        if cuenta_por_cobrar.esta_pagada():
            message = f'Cuenta por cobrar {cuenta_por_cobrar} ha sido pagada en su totalidad.'
            messages.success(self.request, message)
        else:
            message = f'Se registró un pago parcial en la cuenta por cobrar {cuenta_por_cobrar}. Saldo pendiente: {cuenta_por_cobrar.saldo_pendiente}.'
            messages.info(self.request, message)

        # Mensaje de confirmación
        messages.success(self.request, f'Se ha registrado un pago parcial de {form.instance.total} para la venta N° {venta.numero_factura}')
        # Verificar si la solicitud es AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': message})

        # Redirigir al detalle de la venta
        return redirect(self.success_url)
    
        return super().form_valid(form)

    def form_invalid(self, form):
        # Manejar la invalidación del formulario
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})

        messages.error(self.request, 'Error en el registro del recibo de caja. Por favor revisa los datos.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Cargar la venta en el contexto
        venta_id = self.kwargs.get('venta_id')
        context['venta'] = get_object_or_404(Venta, id=venta_id)
        context['title'] = 'Registrar Recibo de Caja2'
        context['entity'] = 'Recibos de Caja'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('ventas:recibo_caja_list')
        return context

    
# Actualizar un recibo de caja
class ReciboCajaUpdateView(UpdateView):
    model = ReciboCaja
    form_class = ReciboCajaForm
    template_name = 'recibo_caja_form.html'
    success_url = reverse_lazy('ventas:recibo_caja_list')

# Eliminar un recibo de caja
class ReciboCajaDeleteView(DeleteView):
    model = ReciboCaja
    template_name = 'recibo_caja_confirm_delete.html'
    success_url = reverse_lazy('ventas:recibo_caja_list')

class ReciboCajaCreate2View(CreateView):
    model = ReciboCaja
    template_name = 'ventas/create2.html'
    form_class = ReciboCajaForm
    success_url = reverse_lazy('ventas:recibo_caja_list')

    def get_success_url(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Recibo de caja registrado exitosamente.'})
        return reverse('ventas:recibo_caja_list')

    @transaction.atomic
    def form_valid(self, form):
        cuentas_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
        monto_pagado = form.cleaned_data['total']  # Total pagado por el cliente

        # Crear el recibo de caja primero con el total en 0 inicialmente
        recibo_caja = form.save(commit=False)
        recibo_caja.total = 0  # El total se actualizará con el monto pagado
        recibo_caja.save()  # Guardamos el recibo para obtener su ID

        # Asignar las cuentas por cobrar utilizando `add()` para ManyToManyField
        recibo_caja.cuenta_por_cobrar.add(*cuentas_por_cobrar)

        # Variables para manejar las cuentas pagadas y pendientes
        cuentas_pagadas = []
        cuentas_pendientes = []
        total_pagado = 0  # Variable para acumular el monto efectivamente pagado

        for cuenta in cuentas_por_cobrar:
            saldo_pendiente = cuenta.saldo_pendiente

            if monto_pagado > 0:
                monto_a_pagar = min(monto_pagado, saldo_pendiente)  # Pagar lo que se pueda de esta cuenta
                cuenta.registrar_pago(recibo_caja, monto_a_pagar)  # Registrar el pago en la cuenta
                monto_pagado -= monto_a_pagar
                total_pagado += monto_a_pagar  # Sumar el monto pagado a la variable acumuladora

                # Guardar en la lista si está pagada o si aún queda saldo pendiente
                if cuenta.esta_pagada():
                    cuentas_pagadas.append(cuenta)
                else:
                    cuentas_pendientes.append(cuenta)

        # Actualizar el total del recibo de caja con el monto efectivamente pagado
        recibo_caja.total = total_pagado
        recibo_caja.save()

        # Mostrar alertas si hay cuentas pendientes
        if cuentas_pendientes:
            msg = f'Las siguientes cuentas quedaron pendientes: {", ".join([str(c) for c in cuentas_pendientes])}'
            messages.warning(self.request, msg)
        else:
            messages.success(self.request, 'Todas las cuentas seleccionadas fueron pagadas.')

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        messages.error(self.request, 'Error en el registro del recibo de caja. Por favor revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Recibo de Caja2'
        context['entity'] = 'Recibos de Caja'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('ventas:recibo_caja_list')
        return context


class ObtenerSaldoCuentaView(View):
    def get(self, request, *args, **kwargs):
        cuenta_id = request.GET.get('cuenta_id')
        if cuenta_id:
            try:
                cuenta = CuentaPorCobrar.objects.get(pk=cuenta_id)
                return JsonResponse({'saldo_pendiente': float(cuenta.saldo_pendiente)})
            except CuentaPorCobrar.DoesNotExist:
                return JsonResponse({'error': 'Cuenta no encontrada'}, status=404)
        return JsonResponse({'error': 'ID de cuenta no proporcionado'}, status=400)