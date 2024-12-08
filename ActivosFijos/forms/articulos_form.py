from django import forms
from ActivosFijos.models.articulos import Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = [
            'Descripcion',
            'codigo',
            'GrupoArticulo_FK',
            'Marca_FK',
            'Modelo',
            'Serie',
            'Area_FK',
            'Observaciones',
            'Costo',
            'Proveedor_FK',
            'TipoArticulo_FK'
        ]

        labels = {
            'Descripcion': 'Descripción',
            'codigo': 'Codigo',
            'GrupoArticulo_FK': 'Grupo de Articulos',
            'Marca_FK': 'Marca',
            'Modelo': 'Modelo',
            'Serie': 'Serie',
            'Area_FK': 'Area de Trabajo (ubicacion)',
            'Observaciones': 'Observaciones',
            'Costo': 'Costo',
            'Proveedor_FK': 'Proveedor',
            'TipoArticulo_FK': 'Tipo de Articulo',
        }
        widgets = {
            'Descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'GrupoArticulo_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'Marca_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'Modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'Serie': forms.TextInput(attrs={'class': 'form-control'}),
            'Area_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'Observaciones': forms.TextInput(attrs={'class': 'form-control'}),
            'Costo': forms.TextInput(attrs={'class': 'form-control'}),
            'Proveedor_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'TipoArticulo_FK': forms.Select(attrs={'class': 'form-control select2'}),
        }

