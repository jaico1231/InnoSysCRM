from django.http import HttpResponse
from django.views import View
from django.template.loader import get_template
from django.views.generic import FormView, ListView, DetailView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Sum
from weasyprint import HTML
from configuracion.models.servicios import Medicos
from shared.models.datos_empresa import DatosIniciales
from shared.models.terceros import Terceros
from ventas.forms.carteraForm import CarteraTerceroForm
from ventas.models.ventas import CuentaPorCobrar


class BuscarCarteraView(FormView):
    template_name = 'cartera/buscar_cartera.html'
    form_class = CarteraTerceroForm
    success_url = '/buscar-cartera/'  # Redirigir a la misma página después de buscar
    pdf_template_name = 'cartera/pdfSaldoCartera.html'

    def form_valid(self, form):
        # Obtener los datos del formulario
        tercero_id = form.cleaned_data.get('tercero')
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        
        # Filtrar cuentas por cobrar según los criterios
        cuentas = CuentaPorCobrar.objects.filter(saldo_pendiente__gt=0)        
        if tercero_id:
            cuentas = cuentas.filter(medico=tercero_id)
        if fecha_inicio and fecha_fin:
            cuentas = cuentas.filter(venta__fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            cuentas = cuentas.filter(venta__fecha__gte=fecha_inicio)
        elif fecha_fin:
            cuentas = cuentas.filter(venta__fecha__lte=fecha_fin)
        # Calcular el total del saldo pendiente
        total_saldo_pendiente = cuentas.aggregate(total=Sum('saldo_pendiente'))['total'] or 0        
        # Actualizar el contexto con los datos de las cuentas por cobrar
        self.terceros = tercero_id
        self.cuentas = cuentas
        datos = self.render_to_response(self.get_context_data(total_saldo_pendiente=total_saldo_pendiente))
        return datos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consulta Cartera'
        context['entity'] = 'Cuentas por Cobrar'
        context['tercero'] = getattr(self, 'tercero', None)
        context['cuentas'] = getattr(self, 'cuentas', [])
        return context

class PDFCarteraView(DetailView):
    model = CuentaPorCobrar

    def get(self, request, pk):
        # Cargar la plantilla HTML
        template = get_template('cartera/pdfSaldoCartera.html')
        # Obtener los parámetros de la URL
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        # Obtener el tercero y la empresa
        medico = Medicos.objects.get(id=pk)
        empresa = DatosIniciales.objects.filter(pk=1).first()
        # Filtrar las cuentas por cobrar
        cuentas = CuentaPorCobrar.objects.filter(saldo_pendiente__gt=0)

        if pk:
            cuentas = cuentas.filter(medico=pk)
        if fecha_inicio and fecha_fin:
            cuentas = cuentas.filter(venta__fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            cuentas = cuentas.filter(venta__fecha__gte=fecha_inicio)
        elif fecha_fin:
            cuentas = cuentas.filter(venta__fecha__lte=fecha_fin)

        # Calcular el saldo total pendiente
        total_saldo_pendiente = cuentas.aggregate(total=Sum('saldo_pendiente'))['total'] or 0

        # Crear el contexto para el template
        context = {
            'medico': medico,
            'cuentas': cuentas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'empresa': empresa,
            'total_saldo_pendiente': total_saldo_pendiente,
        }

        # Renderizar la plantilla con el contexto
        html = template.render(context)

        # Generar el PDF usando WeasyPrint
        pdf = HTML(string=html).write_pdf()

        # Devolver el PDF como respuesta HTTP
        return HttpResponse(pdf, content_type='application/pdf')
   

    # def get(self, request, *args, **kwargs):
    #     template = get_template('cartera/pdfSaldoCartera.html')
    #     context = {
    #         'title': 'Cartera',
    #         'entity': 'Cuentas por Cobrar',
    #         'tercero': kwargs.get('tercero', None),
    #         'cuentas': CuentaPorCobrar.objects.filter(venta__tercero__id=kwargs.get('tercero', None).id)
    #     }
    #     html = template.render(context)
    #     html = HTML(string=html)
    #     result = html.write_pdf()
    #     return HttpResponse(result, content_type='application/pdf')
# vista para crear el pdf
# class ver_carteraView(DetailView):
#     template_name = 'cartera/pdfSaldoCartera.html'
#     model = CuentaPorCobrar
#     # recibe el form_valid de la vista BuscarCarteraView
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Cartera'
#         context['entity'] = 'Cuentas por Cobrar'
#         return context
#     def render_to_response(self, contexto):
#         return self.render_to_pdf(contexto)

class ImprimirCarteraView(DetailView):
    template_name = 'cartera/pdfSaldoCartera.html'
    # recibe el form_valid de la vista BuscarCarteraView
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cartera'
        context['entity'] = 'Cuentas por Cobrar'
        return context




class CuentasPorCobrarListView(ListView):
    model = CuentaPorCobrar
    template_name = 'cartera/buscar_cartera.html'
    context_object_name = 'cuentas'

    def get_queryset(self):
        tercero_id = self.request.session.get('tercero_id')
        if tercero_id:
            return CuentaPorCobrar.objects.filter(medico__id=tercero_id, saldo_pendiente__gt=0)
        return CuentaPorCobrar.objects.none()  # Retorna un queryset vacío si no hay médico seleccionado

# Vista para enviar estado de cuenta
def enviar_estado_cuenta(request, cuenta_id):
    cuenta = CuentaPorCobrar.objects.get(id=cuenta_id)

    # Aquí puedes construir el contenido del correo
    subject = f"Estado de Cuenta para {cuenta.venta.numero_factura}"
    message = f"""
    Estimado {cuenta.venta.tercero.nombre},

    Este es el estado de cuenta correspondiente a la factura {cuenta.venta.numero_factura}.

    Saldo Pendiente: {cuenta.saldo_pendiente}
    Fecha de Vencimiento: {cuenta.fecha_vencimiento}

    Gracias,
    Tu Empresa
    """

    # Enviar el correo (ajusta los parámetros según tu configuración)
    # send_mail(subject, message, 'noreply@tuempresa.com', [cuenta.venta.tercero.email])

    messages.success(request, "Estado de cuenta enviado exitosamente.")
    return redirect('buscar_cartera')  # Redirigir a la vista de búsqueda

