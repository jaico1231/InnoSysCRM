from django import forms
from ActivosFijos.models.areas_trabajo import Areas_Trabajo
class Areas_TrabajoForm(forms.ModelForm):
    class Meta:
        model = Areas_Trabajo
        fields = [
            
            'Descripcion',
            'Observacion',
            'Activo',
        ]

        labels = {
            
            'Descripcion': 'Descripción',
            'Observacion': 'Observación',
            'Activo': 'Activo',
        }
        widgets = {
            'Descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.TextInput(attrs={'class': 'form-control'}),
            'Activo': forms.CheckboxInput(),

        }