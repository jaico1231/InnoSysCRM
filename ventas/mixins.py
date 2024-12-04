from datetime import datetime
from crum import get_current_request
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from django.http import JsonResponse
from configuracion.models.servicios import Medicos, Paquetes, Servicios
from ventas.models.ventas import CuentaPorCobrar

def get_paquete_servicios(request):

    medico_id = request.GET.get('medico_id')
    paquete = Paquetes.objects.filter(paquetes_medicos__medico_id=medico_id).first()
    medico = get_object_or_404(Medicos, pk=medico_id)
    # Obtener todos los campos del paquete
    paquete_data = {
        'id': paquete.id,
        'nombre': paquete.nombre,
        'estado': paquete.estado,
        'codigo': paquete.codigo,
        'precio': paquete.precio
    }
    
    # Obtener todos los campos de los servicios
    servicios_data = []
    for servicio in paquete.paquetes_servicios.all():
        servicio_data = {
            'id': servicio.servicio.id,
            'codigo': servicio.servicio.codigo,
            'nombre': servicio.servicio.nombre,
            'descripcion': servicio.servicio.descripcion,
            'estado': servicio.servicio.estado,
            'precio': servicio.servicio.precio,
            'cantidad': servicio.cantidad
        }
        servicios_data.append(servicio_data)
    medico_descuento = medico.descuento  # Asegúrate de que este campo exista en tu modelo
    medico_comision = medico.comision  # Asegúrate de que este campo exista en tu modelo
    

    
    return JsonResponse({'paquete': paquete_data, 'servicios': servicios_data, 'medico_descuento': medico_descuento, 'medico_comision': medico_comision})

def get_servicios_adicionales(request):

    servicio_id = request.GET.get('servicio_id')
    servicio = get_object_or_404(Servicios, pk=servicio_id)
    return JsonResponse({'servicio': {'id': servicio.id, 'nombre': servicio.nombre, 'precio': servicio.precio, 'codigo': servicio.codigo, 'descuento': servicio.descuento}})

class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context

def obtener_saldo_pendiente(request, cuenta_id):
    try:
        cuenta_por_cobrar = CuentaPorCobrar.objects.get(pk=cuenta_id)
        return JsonResponse({'saldo_pendiente': str(cuenta_por_cobrar.saldo_pendiente)})
    except CuentaPorCobrar.DoesNotExist:
        return JsonResponse({'error': 'Cuenta por Cobrar no encontrada.'}, status=404)

class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('erp:dashboard')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        request = get_current_request()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if 'group' in request.session:
            group = request.session['group']
            perms = self.get_perms()
            for p in perms:
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'No tiene permiso para ingresar a este módulo')
                    return HttpResponseRedirect(self.get_url_redirect())
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())

# class ValidatePermissionRequiredMixin(object):
#     permission_required = ''
#     url_redirect = None
#
#     def get_perms(self):
#         if isinstance(self.permission_required, str):
#             perms = (self.permission_required,)
#         else:
#             perms = self.permission_required
#         return perms
#
#     def get_url_redirect(self):
#         if self.url_redirect is None:
#             return reverse_lazy('index')
#         return self.url_redirect
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.has_perms(self.get_perms()):
#             return super().dispatch(request, *args, **kwargs)
#         messages.error(request, 'No tiene permiso para ingresar a este módulo')
#         return HttpResponseRedirect(self.get_url_redirect())
