from RrHh.models.vacaciones import Vacaciones
from django import forms
import datetime
now = datetime.datetime.now()

class Solicitud_VacacionesForm(forms.ModelForm):
     class Meta:
        model = Vacaciones
        fields = [
            
            # 'colaborador_FK',            
            'fecha_inicial',
            'fecha_final',
        ]
        labels = {
            'fecha_inicial': 'Fecha inicial',
            'fecha_final': 'Fecha final',
        }
        widgets = {
            'fecha_inicial': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'fecha_final': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
        }

class Gestion_VacacionesForm(forms.ModelForm):
    class Meta:
        model = Vacaciones
        fields = [
            # 'colaborador_FK',            
            'fecha_inicial',
            'fecha_final',
            'dias',
            'fecha_inicio_alternativa',
            'fecha_fin_alternativa',
            'dias_alternativo',
            'observaciones',
            'fecha_inicio_laboral',
            'estado',
        ]
        labels = {
            # 'colaborador_FK': 'Colaborador',            
            'fecha_inicial': 'Fecha inicial',
            'fecha_final': 'Fecha final',
            'dias': 'Dias',
            'fecha_inicio_alternativa': 'Fecha inicio alterna',
            'fecha_fin_alternativa': 'Fecha fin alterna',
            'dias_alternativo': 'Dias alterna',
            'observaciones': 'Observaciones',
            'fecha_inicio_laboral': 'Fecha inicio laboral',
            'estado': 'Estado',
        }
        widgets = {
            # 'colaborador_FK': forms.Select(attrs={'class': 'form-control select2'}),            
            'fecha_inicial': forms.TextInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'fecha_final': forms.TextInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'dias': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio_alternativa': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'fecha_fin_alternativa': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'dias_alternativo': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_inicio_laboral': forms.TextInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'estado': forms.Select(attrs={'class': 'form-control select2'}),
        }