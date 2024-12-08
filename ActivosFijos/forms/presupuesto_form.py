from django import forms
from ActivosFijos.models.presupuestos import Presupuestos
class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuestos
        fields = [
            
            'Descripcion',
            'Observacion',
            'cantidad',
            'Activo',
        ]

        labels = {
            
            'Descripcion': 'Descripción',
            'Observacion': 'Observación',
            'cantidad': 'Cantidad',
            'Activo': 'Activo',

        }
        widgets = {
            
            'Descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'Activo': forms.CheckboxInput(),

        }