from django import forms
from ActivosFijos.models.orden_servicio import OrdenServicio
import datetime
now = datetime.datetime.now()
class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = [
            'Tercero',
            'Observaciones',
            'FechaAutorizacion',
            'Solicitante',
            'CreadoPor',
            'Presupuestos',
            'Costo',
            'Autorizado_Por',
            'Estado',
            'Observaciones_adicionales',
        ]
        labels = {
            'Tercero': 'Tercero',
            'Observaciones': 'Observaciones',
            'FechaAutorizacion': 'Fecha de Autorizacion',
            'Solicitante': 'Solicitante',
            'CreadoPor': 'Creado Por',
            'Presupuestos': 'Presupuestos',
            'Costo': 'Costo',
            'Autorizado_Por': 'Autorizado Por',
            'Estado': 'Estado',
            'Observaciones_adicionales': 'Observaciones adicionales',
        }
        widgets = {
            'Tercero': forms.Select(attrs={'class': 'form-select select2'}),
            'Observaciones': forms.TextInput(attrs={'class': 'form-control'}),
            'FechaAutorizacion' : forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'Solicitante': forms.Select(attrs={'class': 'form-select select2'}),
            'CreadoPor': forms.Select(attrs={'class': 'form-select select2'}),
            'Presupuestos': forms.Select(attrs={'class': 'form-control select2'}),
            'Costo': forms.TextInput(attrs={'class': 'form-control'}),
            'Autorizado_Por': forms.Select(attrs={'class': 'form-control select2'}),
            'Estado': forms.Select(attrs={'class': 'form-select select2'}),
            'Observaciones_adicionales': forms.TextInput(attrs={'class': 'form-control'}),
        }