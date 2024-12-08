from django import forms
from Comercial.models import Cotizacion, DetalleCotizacion
from Produccion.models.Proceso_Produccion import ProductoTerminado

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }
  

class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class NuevoProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = ['nombre', 'descripcion', 'precio']