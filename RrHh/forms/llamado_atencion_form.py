from django import forms
from RrHh.models.llamado_atencion import *
from datetime import date
now = date.today()

class Llamado_AtencionForm(forms.ModelForm):
    
    class Meta:
        model = Llamado_Atencion
        fields = {'colaborador',
                  'fecha_infraccion',
                  'Autorizado_por',
                  'acciones'
                  }
        labels = {
            'colaborador': 'Colaborador',
            'fecha_infraccion': 'Fecha Infracción',
            'Autorizado_por': 'Autorizado Por',
            'acciones': 'Acciones',
        }
        widgets = {
            'fecha_infraccion': forms.TextInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'Autorizado_por': forms.Select(attrs={'class': 'select2'}),
            'colaborador': forms.Select(attrs={'class': 'select2'}),
            'acciones': forms.Textarea(attrs={'rows': 3}),
        }

class DescargosForm(forms.ModelForm):
    
    class Meta:
        model = Descargos
        fields = {
                #   'fecha_descargo',
                  'autorizado_por',
                #   'Llamado_Atencion',
                  'acciones'
                  }
        labels = {
            # 'fecha_descargo': 'Fecha Descargo',
            'autorizado_por': 'Entrevistador',
            # 'Llamado_Atencion': 'Llamado Atención',
            'acciones': 'Motivos de los Descargos',
        }
        widgets = {
            # 'fecha_descargo': forms.TextInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'autorizado_por': forms.Select(attrs={'class': 'select2'}),
            # 'Llamado_Atencion': forms.Select(attrs={'class': 'select2'}),
            'acciones': forms.Textarea(attrs={'rows': 6}),
        }

class Cuestionario_DescargosForm(forms.ModelForm):    
    class Meta:
        model = Cuestionario_Descargos
        fields = {
            'Descargos_FK',
            'preguntas',
            'respuestas',
            'anexos'
        }
        labels = {
            'Descargos_FK': 'Descargos',
            'preguntas': 'Preguntas',
            'respuestas': 'Respuestas',
            'anexos': 'Anexos'
        }
        widgets = {
            'Descargos_FK': forms.Select(attrs={'class': 'select2'}),
            'preguntas': forms.Textarea(attrs={'rows': 3}),
            'respuestas': forms.Textarea(attrs={'rows': 3}),
            'anexos': forms.FileInput(attrs={'class': 'form-control'}),
        }