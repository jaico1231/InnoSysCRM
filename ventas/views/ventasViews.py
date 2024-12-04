from datetime import datetime, timedelta
import json
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from decimal import Decimal
from django.core import serializers
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,FormView,DetailView
from shared.loggin import log_event
from shared.mixins import PDFTemplateMixin
from shared.models.datos_empresa import DatosIniciales
from ventas.forms.ventasForm import VentaForm, VentaServiciosForm
from configuracion.models.servicios import  Medico_paquetes, Servicios, Paquetes, Medicos
from ventas.models.ventas import CuentaPorCobrar, ReciboCaja, VentaServicios, Venta
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class VentaListView(ListView):
    # permission_required = 'ventas.view_venta'
    model = Venta
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['entity'] = 'Ventas'
        context['headers'] = ['N°', 'FECHA', 'TERCERO', 'DOCTOR',  'TOTAL']
        context['fields'] = ['numero_factura', 'fecha',  'tercero', 'medico','total']
        context['actions'] = [
            {
                'name': 'detali',
                'icon': 'print',
                'label': '',
                'color': 'success',
                'color2': 'white',
                'url': 'ventas:print-venta-pdf',
                
            },
            {
            'name': 'block',
            'icon': 'disabled_by_default',
            'label': '',
            'color': 'secondary',
            'color2': 'white',
            'url': 'ventas:ver_factura',
            # 'modal': 'Activar',
        }
        ]
        context['list_url'] = reverse_lazy('ventas:crear-venta')
        return context

class VentaCreateView(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('ventas:crear-venta')

    
    @transaction.atomic
    def form_valid(self, form):
        # Guardar los datos de la venta sin realizar el commit todavía
        venta = form.save(commit=False)

        # Depuración: Verificar si el formulario contiene el campo tipo_transaccion
        print(f'Formulario: {form.cleaned_data}')
        print(f'Tipo de transacción desde el formulario: {form.cleaned_data.get("tipo_transaccion")}')

        # Inicializar los campos de la venta
        venta.subtotal = Decimal('0')
        venta.impuestos = Decimal('0')
        venta.descuentos = Decimal('0')
        venta.total = Decimal('0')

        medico = form.cleaned_data['medico']
        
        # Capturar los servicios adicionales
        servicios_adicionales_json = self.request.POST.get('servicios_adicionales_json')
        servicios_adicionales = json.loads(servicios_adicionales_json) if servicios_adicionales_json else []

        # Depuración: Verificar si el campo tipo_transaccion se ha guardado correctamente en la venta
        print(f'Tipo de transacción en la venta: {venta.tipo_transaccion}')

        # Crear la transacción correspondiente
        self.create_tipo_transaccion(venta)

        # Agregar los servicios del paquete del médico, si existe
        paquete = Paquetes.objects.filter(paquetes_medicos__medico=medico).first()
        if paquete:
            self.add_package_services(venta, paquete, medico)

        # Agregar servicios adicionales
        self.add_additional_services(venta, servicios_adicionales)

        # Guardar la venta con todos los servicios añadidos
        venta.save()

        # Actualizar los totales de la venta
        self.update_venta_totals(venta)

        

        # Registrar en el log que la venta fue creada
        log_event(self.request.user, 'info', f'Se registró una venta a {venta.tercero} por un total de {venta.total}')
        
        messages.success(self.request, f'Venta registrada correctamente. Total: {venta.total}')
        return super().form_valid(form)

    

    def add_package_services(self, venta, paquete, medico):
        for paquete_servicio in paquete.paquetes_servicios.all():
            servicio = paquete_servicio.servicio
            cantidad = paquete_servicio.cantidad
            precio_original = servicio.precio
            descuento = medico.descuento or Decimal('0')
            precio_con_descuento = precio_original * (1 - descuento / 100)

            VentaServicios.objects.create(
                venta=venta,
                servicio=servicio,
                cantidad=cantidad,
                precio=precio_con_descuento,
                descuento=descuento,
                total=precio_con_descuento * cantidad
            )

    def add_additional_services(self, venta, servicios_adicionales):
        for servicio_id in servicios_adicionales:
            servicio = get_object_or_404(Servicios, pk=servicio_id)
            VentaServicios.objects.create(
                venta=venta,
                servicio=servicio,
                cantidad=1,
                precio=servicio.precio,
                descuento=Decimal('0'),
                total=servicio.precio
            )

    def update_venta_totals(self, venta):
        venta_servicios = venta.venta_servicios.all()
        venta.subtotal = sum(vs.total for vs in venta_servicios)
        venta.descuentos = sum(vs.precio * vs.cantidad * vs.descuento / 100 for vs in venta_servicios)

        # Aplicar una tasa de impuestos fija del 19% (ajustar según sea necesario)
        venta.impuestos = venta.subtotal * Decimal('0.19')
        venta.total = venta.subtotal + venta.impuestos - venta.descuentos
        venta.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = VentaServiciosForm()  # Formulario de servicios
        context['medicos'] = Medicos.objects.all()
        context['title'] = 'Registrar Venta'
        context['entity'] = 'Ventas'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('shared:terceros')

        # Verificar si hay un médico seleccionado para mostrar los servicios relacionados
        medico_id = self.request.GET.get('medico_id')
        if medico_id:
            medico = get_object_or_404(Medicos, pk=medico_id)
            paquete = Paquetes.objects.filter(paquetes_medicos__medico=medico).first()
            print('get_context_data', paquete)
            if paquete:
                # Servicios del paquete relacionado con el médico
                context['paquete_servicios'] = paquete.paquetes_servicios.all()

            # Obtener los servicios adicionales seleccionados en el formulario
            servicios_adicionales = self.request.GET.getlist('servicios_adicionales')
            if servicios_adicionales:
                context['servicios_adicionales'] = Servicios.objects.all()

        return context

    def get_additional_services(self):
        servicios_adicionales = self.request.POST.getlist('servicios_adicionales')
        print('get_additional_services', servicios_adicionales)
        return Servicios.objects.filter(id__in=servicios_adicionales)

def ruta_venta_create(request):
    medico_id = request.GET.get('medico_id')
    if medico_id:
        medico = get_object_or_404(Medicos, pk=medico_id)
        paquete = Paquetes.objects.filter(paquetes_medicos__medico=medico).first()
        if paquete:
            servicios = paquete.paquetes_servicios.all()

            # Calcular precio con descuento y total en la vista
            servicios_con_descuento = []
            for servicio in servicios:
                precio_original = servicio.servicio.precio
                descuento = medico.descuento or 0  # Si no hay descuento, se asume 0
                precio_con_descuento = precio_original * (1 - descuento / 100)
                total = precio_con_descuento * servicio.cantidad
                servicios_con_descuento.append({
                    'servicio': servicio,
                    'precio_original': precio_original,
                    'precio_con_descuento': precio_con_descuento,
                    'total': total
                })

            # Renderiza los servicios y pasa el médico y los cálculos al contexto
            return render(request, 'ventas/partials/servicios_table.html', {
                'servicios_con_descuento': servicios_con_descuento,
                'medico': medico
            })
    
    # En caso de no haber servicios, devuelve una tabla vacía
    return render(request, 'ventas/partials/servicios_table.html', {
        'servicios_con_descuento': [],
        'medico': None
    })

def buscar_servicios(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        servicios = Servicios.objects.filter(nombre__icontains=query)
        data = serializers.serialize('json', servicios)
        return HttpResponse(data, content_type='application/json')

def guardar_venta(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        numero_factura = request.POST.get('numero_factura')
        tercero_id = request.POST.get('tercero')
        medico_id = request.POST.get('medico')
        metodo_pago_id = request.POST.get('metodo_pago')
        tipo_transaccion_id = request.POST.get('tipo_transaccion')
        subtotal = request.POST.get('subtotal')
        servicios_json = request.POST.get('servicios_json')
        fecha = request.POST.get('fecha')
    
        try:
            fecha_venta = datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            # Manejar el error en caso de que la fecha no sea válida
            return render(request, 'ventas/form_venta.html', {'error': 'Fecha no válida'})

        if Venta.objects.filter(numero_factura=numero_factura).exists():
            messages.error(request, 'El número de factura ya está registrado se cancela el registro.')  # Mensaje de error
            return redirect('ventas:crear-venta')
        # Parsear el JSON de los servicios
        
        servicios_data = json.loads(servicios_json)

        # Crear el registro de la venta
        venta = Venta.objects.create(
            numero_factura=numero_factura,
            tercero_id=tercero_id,
            medico_id=medico_id,
            metodo_pago_id=metodo_pago_id,
            tipo_transaccion_id=tipo_transaccion_id,
            subtotal=subtotal,
            total=subtotal,  # Ajusta según sea necesario
            fecha=fecha_venta  # Guardar la fecha de la venta
        )
        
        if int(tipo_transaccion_id) == 2:
            
            # Crear una cuenta por cobrar
            CuentaPorCobrar.objects.create(
                venta=venta,
                medico=venta.medico,
                fecha_vencimiento=(datetime.now() + timedelta(days=30)).date(),  # 30 días de plazo
                saldo_pendiente=venta.total
            )
        if int(tipo_transaccion_id) == 1:
            
            # Crear un recibo de caja
            ReciboCaja.objects.create(
                ventas=venta,
                fecha=venta.fecha,
                metodo_pago=venta.metodo_pago,
                total=venta.total
            )
        # Guardar cada servicio en la tabla de DetalleVenta
        for servicio_data in servicios_data:
            servicio = Servicios.objects.get(codigo=servicio_data['codigo'])
            VentaServicios.objects.create(
                venta=venta,
                servicio=servicio,
                cantidad=servicio_data['cantidad'],
                precio=servicio_data['precio_unitario'],                
                descuento=servicio_data['descuento'],
                total=servicio_data['precio_final'],
            )
                
        # Redirigir o enviar una respuesta
        return redirect('ventas:crear-venta' )  # Redirige a la lista de ventas

    return redirect('ventas:crear-venta' )
class ver_factura(DetailView):
    template_name = 'ventas/reporte_venta_pdf.html'
    model = Venta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Factura'
        context['empresa'] = get_object_or_404(DatosIniciales, pk=1)
        if context['venta'].medico:
            context['paquete'] = Medico_paquetes.objects.filter(medico=context['venta'].medico).first().paquete        
        context['venta'] = self.get_object()  # Ya puedes usar self.get_object() que obtiene la venta
        context['servicios'] = VentaServicios.objects.filter(venta=context['venta'])
        return context

class ImprimirFacturaView(PDFTemplateMixin, View):
    pdf_template_name = 'ventas/reporte_venta_pdf.html'
    #revizar las consultas 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Factura'
        context['venta'] = Venta.objects.get(pk=self.kwargs['pk'])
        context['servicios'] = VentaServicios.objects.filter(venta=self.kwargs['pk'])
        print(context['venta'])
        print(context['servicios'])
        return context

        # Crear el contexto con los datos de la venta
