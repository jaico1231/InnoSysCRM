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
# class ReciboCajaCreateView(CreateView):
#     model = ReciboCaja
#     form_class = ReciboCajaForm
#     template_name = 'shared/create_no_modal.html'

#     def get_success_url(self):
#         if self.request.accepts('application/json'):
#             return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
#         else:
#             return reverse_lazy('ventas:recibo_caja_list')  # Ajusta según tu URL de éxito
    
#     @transaction.atomic
#     def form_valid(self, form):
#         recibo_caja = form.save(commit=False)
#         cuenta_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
#         monto_pagado = form.cleaned_data['total']

#         # Registrar el pago en la cuenta por cobrar
#         cuenta_por_cobrar.registrar_pago(recibo_caja, monto_pagado)
#         recibo_caja.save()

#         # Mensaje por estado de la cuenta por cobrar
#         if cuenta_por_cobrar.esta_pagada():
#             messages.success(self.request, 'La cuenta por cobrar ha sido pagada.')
#         else:
#             messages.warning(self.request, 'La cuenta por cobrar no ha sido pagada.')

#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         # Si el formulario no es válido, muestra los errores en el template
#         messages.error(self.request, 'Error en el registro del recibo de caja. Por favor revisa los datos.')
#         return super().form_invalid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Registrar Caja'
#         context['entity'] = 'Recibos de Caja'
#         return context
# class ReciboCajaCreateView(CreateView):
#     model = ReciboCaja
#     form_class = ReciboCajaForm
#     template_name = 'ReciboCaja/create.html'
#     def get_success_url(self):
#         if self.request.accepts('application/json'):
#             return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
#         else:
#             return reverse_lazy('ventas:recibo_caja_list')  # Ajusta según tu URL de éxito
#     @transaction.atomic
#     def form_valid(self, form):
#         recibo_caja = form.save(commit=False)
#         cuenta_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
#         monto_pagado = form.cleaned_data['total']
        
#         # Registrar el pago en la cuenta por cobrar
#         cuenta_por_cobrar.registrar_pago(recibo_caja, monto_pagado)
#         recibo_caja.save()

#         # Mensaje según el estado de la cuenta por cobrar
#         if cuenta_por_cobrar.esta_pagada():
#             message = f'Cuenta por cobrar {cuenta_por_cobrar} ha sido pagada en su totalidad.'
#             messages.success(self.request, message)
#         else:
#             message = f'Se registró un pago parcial en la cuenta por cobrar {cuenta_por_cobrar}. Saldo pendiente: {cuenta_por_cobrar.saldo_pendiente}.'
#             messages.info(self.request, message)

#         # Verificar si la solicitud es AJAX
#         if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({'success': True, 'message': message})

#         return super().form_valid(form)
#     # def form_valid(self, form):
#     #     cuenta_por_cobrar_ids = [form.cleaned_data.get('cuenta_por_cobrar')]  # Lista de IDs de cuentas seleccionadas
#     #     metodo = form.cleaned_data.get('metodo_pago')
#     #     fecha = form.cleaned_data.get('fecha')
#     #     total_pago = form.cleaned_data.get('total')
#     #     observaciones = form.cleaned_data.get('observaciones')
#     #     print(metodo)

#     #     total_saldo_a_pagar = total_pago

#         # for cuenta_id in cuenta_por_cobrar_ids:
#         #     cuenta = CuentaPorCobrar.objects.get(id=cuenta_id)

#         #     if total_saldo_a_pagar <= 0:
#         #         break

#         #     if cuenta.saldo_pendiente > 0:
#         #         if cuenta.saldo_pendiente <= total_saldo_a_pagar:
#         #             # Pagar la factura en su totalidad
#         #             total_saldo_a_pagar -= cuenta.saldo_pendiente
#         #             cuenta.saldo_pendiente = 0  # Saldo a cero
#         #         else:
#         #             # Pagar parcialmente la factura
#         #             cuenta.saldo_pendiente -= total_saldo_a_pagar
#         #             total_saldo_a_pagar = 0  # Saldo restante a cero

#         #         cuenta.save()  # Guardar cambios en la cuenta

#         # # Crear el recibo de caja
#         # recibo_caja = form.save(commit=False)
#         # recibo_caja.total = total_pago - total_saldo_a_pagar  # Total pagado (puede ser menor si hay saldo a favor)
#         # recibo_caja.observaciones = observaciones
#         # recibo_caja.save()

#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Registrar Recibo de Caja'
#         context['entity'] = 'Recibos de Caja'
#         context['action'] = 'add'
#         context['list_url'] = reverse_lazy('ventas:recibo_caja_list')
#         return context

# # Crear un nuevo recibo de caja
# # class ReciboCajaCreateView(CreateView):
# #     model = ReciboCaja
# #     form_class = ReciboCajaForm
# #     template_name = 'shared/create_no_modal.html'
# #     success_url = reverse_lazy('ventas:recibo_caja_list')  # Ajusta según tu URL de éxito
# #     def form_valid(self, form):
# #         # Obtener los datos seleccionados en el formulario
# #         cuenta_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
# #         metodo = form.cleaned_data['metodo_pago']
# #         fecha = form.cleaned_data['fecha']
# #         total = form.cleaned_data['total']
# #         observaciones = form.cleaned_data['observaciones']
# #         print (cuenta_por_cobrar,metodo, fecha, total, observaciones)

#     # def form_valid(self, form):
#     #     # Obtener la cuenta por cobrar asociada
#     #     cuenta_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
#     #     total_pagado = form.cleaned_data['total']
        
#     #     # Registrar el pago en la cuenta por cobrar
#     #     cuenta_por_cobrar.registrar_pago(total_pagado)

#     #     # Verificar si la cuenta está pagada por completo
#     #     if cuenta_por_cobrar.esta_pagada():
#     #         messages.success(self.request, f'Cuenta por cobrar {cuenta_por_cobrar} ha sido pagada en su totalidad.')
#     #     else:
#     #         messages.info(self.request, f'Se registró un pago parcial en la cuenta por cobrar {cuenta_por_cobrar}. Saldo pendiente: {cuenta_por_cobrar.saldo_pendiente}.')

#     #     # Llamar al método form_valid para continuar con el flujo normal y guardar el recibo de caja
#     #     return super().form_valid(form)

#     # def form_invalid(self, form):
#     #     # Si el formulario no es válido, muestra los errores en el template
#     #     messages.error(self.request, 'Error en el registro del recibo de caja. Por favor revisa los datos.')
#     #     return super().form_invalid(form)
# class ReciboCajaCreate2View(CreateView):
#     model = ReciboCaja
#     form_class = ReciboCajaForm
#     template_name = 'shared/create_no_modal.html'
#     success_url = reverse_lazy('ventas:recibo_caja_list')  # Ajusta según tu URL de éxito

#     def form_valid(self, form):
#         pass
# # class ReciboCajaCreate2View(CreateView):
# #     model = ReciboCaja
# #     template_name = 'shared/create_no_modal.html'
# #     form_class = ReciboCajaForm

# #     def get_success_url(self):
# #         # Comprobar si la solicitud es AJAX
# #         if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
# #             return JsonResponse({'success': True, 'message': 'Recibo de caja registrado exitosamente.'})
# #         # Para solicitudes normales, redirigir a la URL de éxito estándar
# #         return reverse('ventas:recibo_caja_list')  # Cambia esto por el nombre correcto de la URL
# #     @transaction.atomic
# #     def form_valid(self, form):
# #         # Recibe los datos del formulario teniendo en cuenta las cuentas por cobrar seleccionadas
# #         # y el monto total del pago

# #         # Obtener las cuentas por cobrar seleccionadas
# #         cuenta_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
# #         print("las cuentas recibidas son:",cuenta_por_cobrar)


# #         # recibo_caja = form.save(commit=False)
# #         # ventas = form.cleaned_data['cuenta_por_cobrar']  # Ventas seleccionadas (cuentas por cobrar)
# #         # print("las ventas recibidas son:",ventas)
# #         # monto_pagado = form.cleaned_data['total']  # Monto total del pago
# #         # total_saldo_pendiente = ventas.aggregate(total=Sum('saldo_pendiente'))['total'] or 0

# #         # Verificar si el monto total pagado excede el saldo pendiente de las cuentas
# #         # if monto_pagado > total_saldo_pendiente:
# #         #     form.add_error('total', 'El monto pagado excede el saldo pendiente.')
# #         #     return self.form_invalid(form)

# #         # # Repartir el pago proporcionalmente entre las cuentas por cobrar
# #         # for venta in ventas:
# #         #     saldo_pendiente = venta.saldo_pendiente
# #         #     if saldo_pendiente > 0:
# #         #         if monto_pagado >= saldo_pendiente:
# #         #             monto_a_pagar = saldo_pendiente
# #         #         else:
# #         #             monto_a_pagar = monto_pagado

# #         #         # Registrar el pago en la cuenta por cobrar
# #         #         venta.registrar_pago(recibo_caja, monto_a_pagar)
# #         #         monto_pagado -= monto_a_pagar

# #         #         if monto_pagado <= 0:
# #         #             break  # Detener si se ha cubierto todo el monto pagado

# #         # recibo_caja.save()

# #         # # Verificar si la solicitud es AJAX
# #         # if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
# #         #     return JsonResponse({'success': True, 'message': 'Recibo de caja registrado exitosamente.'})

# #         # messages.success(self.request, 'Recibo de caja registrado exitosamente.')
# #         return super().form_valid(form)
# #     # @transaction.atomic
# #     # def form_valid(self, form):
# #     #     recibo_caja = form.save(commit=False)
# #     #     cuenta_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
# #     #     monto_pagado = form.cleaned_data['total']
        
# #     #     # Registrar el pago en la cuenta por cobrar
# #     #     cuenta_por_cobrar.registrar_pago(recibo_caja, monto_pagado)
# #     #     recibo_caja.save()

# #     #     # Mensaje según el estado de la cuenta por cobrar
# #     #     if cuenta_por_cobrar.esta_pagada():
# #     #         message = f'Cuenta por cobrar {cuenta_por_cobrar} ha sido pagada en su totalidad.'
# #     #         messages.success(self.request, message)
# #     #     else:
# #     #         message = f'Se registró un pago parcial en la cuenta por cobrar {cuenta_por_cobrar}. Saldo pendiente: {cuenta_por_cobrar.saldo_pendiente}.'
# #     #         messages.info(self.request, message)

# #     #     # Verificar si la solicitud es AJAX
# #     #     if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
# #     #         return JsonResponse({'success': True, 'message': message})

# #     #     return super().form_valid(form)

#     def form_invalid(self, form):
#         # Manejar la invalidación del formulario
#         if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             print("error en el formulario")
#             return JsonResponse({'success': False, 'errors': form.errors})

        

#         messages.error(self.request, 'Error en el registro del recibo de caja. Por favor revisa los datos.')
#         return super().form_invalid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Registrar Recibo de Caja2'
#         context['entity'] = 'Recibos de Caja'
#         context['action'] = 'add'
#         context['list_url'] = reverse_lazy('ventas:recibo_caja_list')
#         return context

    
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
        # Comprobar si la solicitud es AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Comprobar si es una solicitud AJAX
            return JsonResponse({'success': True, 'message': 'Recibo de caja registrado exitosamente.'})
        else:
            return reverse('ventas:recibo_caja_list')  # Correcto uso de reverse para URL normal
    @transaction.atomic
    def form_valid(self, form):
        # Obtener las cuentas seleccionadas y el monto total del pago
        cuentas_por_cobrar = form.cleaned_data['cuenta_por_cobrar']  # Varias cuentas
        monto_pagado = form.cleaned_data['total']

        # Dividir el monto pagado entre las cuentas seleccionadas
        for cuenta in cuentas_por_cobrar:
            saldo_pendiente = cuenta.saldo_pendiente

            # Registrar el pago en cada cuenta por cobrar (si el monto pagado alcanza)
            if monto_pagado > 0:
                monto_a_pagar = min(monto_pagado, saldo_pendiente)  # Se paga lo que se pueda de cada cuenta
                cuenta.registrar_pago(monto_a_pagar)
                monto_pagado -= monto_a_pagar

        return super().form_valid(form)

    def form_invalid(self, form):
        # Manejar la invalidación del formulario en solicitudes AJAX
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
        

    # @transaction.atomic
    # def form_valid(self, form):
    #     # recibo_caja = form.save(commit=False)
    #     # cuenta_por_cobrar = form.cleaned_data['cuenta_por_cobrar']
    #     # monto_pagado = form.cleaned_data['total']
    #     # print(cuenta_por_cobrar)
    #     print("hola")
    #     return super().form_valid(form)
    #     # # Registrar el pago en la cuenta por cobrar
    #     # cuenta_por_cobrar.registrar_pago(recibo_caja, monto_pagado)
    #     # recibo_caja.save()
    #     # # Mensaje según el estado de la cuenta por cobrar
    #     # if cuenta_por_cobrar.esta_pagada():
    #     #     message = f'Cuenta por cobrar {cuenta_por_cobrar} ha sido pagada en su totalidad.'
    #     #     messages.success(self.request, message)
    #     # else:
    #     #     message = f'Se registró un pago parcial en la cuenta por cobrar {cuenta_por_cobrar}. Saldo pendiente: {cuenta_por_cobrar.saldo_pendiente}.'
    #     #     messages.info(self.request, message)
    #     # def form_invalid(self, form):
    #     # # Manejar la invalidación del formulario
    #     #     if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     #         return JsonResponse({'success': False, 'errors': form.errors})

    #     #     messages.error(self.request, 'Error en el registro del recibo de caja. Por favor revisa los datos.')
    #     #     return super().form_invalid(form)  
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Registrar Recibo de Caja2'
    #     context['entity'] = 'Recibos de Caja'
    #     context['action'] = 'add'
    #     context['list_url'] = reverse_lazy('ventas:recibo_caja_list')
    #     return context
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