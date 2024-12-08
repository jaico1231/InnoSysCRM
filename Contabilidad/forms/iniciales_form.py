from Contabilidad.models.retroactivo import *
from Contabilidad.models.conceptos import *
from django import forms
#como usar esos widgets
# from django.contrib.admin.widgets import FilteredSelectMultiple
# from django.utils.translation import gettext_lazy as _

class PreciosRutaForm(forms.ModelForm):

    class Meta:
        model = Tabla_Precios_Rutas
        fields = (
            'nombre',
            'kmh',
            'valor',
            'descripcion'
        )

        labels = {
            'Nombre': 'Nombre de la Ruta',
            'valor': 'Precios',
            'kmh': 'Distancia en Kilometros',
            'descripcion': 'Descripción'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ruta': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'kmh': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'})
        }

class HorasExtrasForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionHorasExtras
        fields = (
            'nombre',
            'codigo',
            'porcentaje'
        )

        labels = {
            'nombre': 'Nombre',
            'codigo': 'Código',
            'porcentaje': 'Porcentaje'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'form-control'})
        }