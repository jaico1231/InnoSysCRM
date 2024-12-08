from django import forms
from ActivosFijos.models.hoja_vida_articulo import Hoja_Vida_Articulos
class Hoja_Vida_ArticulosForm(forms.ModelForm):
    class Meta:
        model = Hoja_Vida_Articulos
        fields = [
            'Articulo_FK',
            'Actualizacion',
            'Novedad',
        ]

        labels = {
            'Articulo_FK': 'Articulo',
            'Actualizacion': 'Actualizacion',
            'Novedad': 'Novedad',
        }
        widgets = {
            'Articulo_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'Actualizacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
