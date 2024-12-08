from django import forms
from ActivosFijos.models.anexo_articulo import Anexos_Articulos

class Anexos_ArticuloForm(forms.ModelForm):
    class Meta:
        model = Anexos_Articulos
        fields = [
            'TipoAnexo',
            'Archivo',
        ]

        labels = {
            'TipoAnexo': 'Tipo de anexo',
            'Archivo': 'Archivo',
        }
        widgets = {
            'TipoAnexo': forms.Select(attrs={'class': 'form-control select2'}),
            'Archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }
