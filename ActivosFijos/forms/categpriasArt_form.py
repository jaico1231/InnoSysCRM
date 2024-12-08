from django import forms

from ActivosFijos.models.categoria_articulos import Categoria_Articulo

class Categoria_Articulo_Form(forms.ModelForm):
    class Meta:
        model = Categoria_Articulo
        fields = [
            'Descripcion',
            'Observacion',
            'Estado',
        ]

        labels = {
            'Descripcion': 'Descripción',
            'Observacion': 'Observación',
            'Estado': 'Estado',
        }

        widgets = {
            'Descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.TextInput(attrs={'class': 'form-control'}),
            'Estado': forms.Select(attrs={'class': 'form-control select2'}),
        }