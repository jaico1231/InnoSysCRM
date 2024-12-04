from django import forms
from django.db.models import Max
from configuracion.models.servicios import Servicios
from shared.models.tipo_pago import TipoPago, TipoTransaccion
from ventas.models.ventas import Venta, VentaServicios
from datetime import datetime
now = datetime.now()

numeros_factura = Venta.objects.values_list('numero_factura', flat=True)
if not numeros_factura:
    consecutivo = 1
else:
# Filtrar los números de factura para asegurarse de que no estén vacíos
    numeros_factura_validos = [numero for numero in numeros_factura if numero]

    # Obtener el número más alto de la lista filtrada
    if numeros_factura_validos:
        numero_mas_alto = max(numeros_factura_validos)

    consecutivo = numero_mas_alto + 1
class VentaForm(forms.ModelForm):
    servicios_adicionales = forms.ModelMultipleChoiceField(
        queryset=Servicios.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        required=False
    )
    
    class Meta:
        model = Venta
        fields = ['tercero', 'medico','fecha', 'numero_factura',  'metodo_pago','subtotal', 'impuestos','descuentos', 'total', 'observaciones', 'tipo_transaccion']

        labels = {
            'tercero': 'Tercero',
            'medico': 'Remitido por',
            'fecha': 'Fecha',
            'numero_factura': 'N° Factura',
            'metodo_pago': 'Método de Pago',
            'subtotal': 'Subtotal',
            'impuestos': 'IVA',
            'descuentos': 'Descuentos',
            'total': 'Total',
            'observaciones': 'Observaciones',
            'tipo_transaccion': 'Tipo de Transacción',
        }        
        widgets = {
            'tercero': forms.Select(attrs={'class': 'form-control select2'}),
            'medico': forms.Select(attrs={'class': 'form-control select2', 'onchange': 'loadPaqueteServicios();'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control select2'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'impuestos': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'descuentos': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_transaccion': forms.Select(attrs={'class': 'form-control select2'}),
        }

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        # Establecer la fecha actual como valor predeterminado si el formulario es nuevo
        if 'fecha' not in self.initial:
            self.initial['fecha'] = datetime.now().strftime('%Y-%m-%d')
        self.fields['fecha'].widget = forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'value': self.initial.get('fecha', ''),  # Asegura que se pase la fecha formateada
            'min': '1900-01-01',
        })
        
        if 'numero_factura' not in self.initial:
            self.initial['numero_factura'] = consecutivo
        self.fields['numero_factura'].widget = forms.TextInput(attrs={'class': 'form-control', 'unique':'true' ,'value': self.initial.get('numero_factura', '')})            
        # if 'metodo_pago' not in self.initial:
        #     self.initial['metodo_pago'] = TipoPago.objects.get(nombre='Pendiente')
        if 'tipo_transaccion' not in self.initial:
            self.initial['tipo_transaccion'] = TipoTransaccion.objects.get(nombre='CREDITO')
            


class VentaServiciosForm(forms.ModelForm):
    class Meta:
        model = VentaServicios
        fields = [ 'servicio', 'cantidad','precio', 'descuento', 'total']

        labels = {
            'servicio': 'Servicio',
            'cantidad': 'Examen',
            'precio': 'Precio',
            'descuento': 'Descuento',
            'total': 'Total',
        }

        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
    