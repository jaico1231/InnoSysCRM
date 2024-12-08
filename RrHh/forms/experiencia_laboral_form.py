from django import forms
from RrHh.models.experiencia_laboral import experiencia_laboral
import datetime
now = datetime.datetime.now()

class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = experiencia_laboral
        fields = [
            'empresa_EXP',
            'cargo_EXP',
            'fecha_inicio_EXP',
            'fecha_fin_EXP',            
            ]
        labels = {
            'empresa_EXP': 'Empresa',
            'cargo_EXP': 'Cargo',
            'fecha_inicio_EXP': 'Fecha de inicio',
            'fecha_fin_EXP': 'Fecha de fin',
        }
        widgets = {
            'empresa_EXP': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo_EXP': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio_EXP': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'fecha_fin_EXP': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            }
