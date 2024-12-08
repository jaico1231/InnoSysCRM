from django import forms
from shared.models.user import User
from RrHh.models.hoja_vida import Hoja_Vida
from RrHh.models.tipo_formato_carta import Tipo_Formato_Carta
from RrHh.models.creacion_documentos import Creacion_Documentos

class Cartas_Form(forms.ModelForm):
    class Meta:
        model = Creacion_Documentos
        fields = [
            'colaborador_FK', 
            'Tipo_Formato_CartaFK', 
            'propietario_doc',
            'fecha_inicio_vacacion',
            'fecha_fin_vacacion',
            'dias_vacaciones',
            'fecha_inicio_alternativa',
            'fecha_fin_alternativa',
            'dias_alternativo',
            'observaciones',
            'accion_irregular',
            'reportes_anexos',
            'estado',
            ]
        labels = {
            'colaborador_FK': 'Colaborador',
            'Tipo_Formato_CartaFK': 'Tipo Formato',
            'propietario_doc': 'Solicitante',
            'fecha_inicio_vacacion': 'Fecha inicio vacaciones',
            'fecha_fin_vacacion': 'Fecha fin vacaciones',
            'dias_vacaciones': 'Dias vacaciones',
            'fecha_inicio_alternativa': 'Fecha inicio alterna',
            'fecha_fin_alternativa': 'Fecha fin alterna',
            'dias_alternativo': 'Dias alterna',
            'observaciones': 'Observaciones',
            'accion_irregular': 'Accion irregular',
            'reportes_anexos': 'Reportes anexos',
            'estado': 'Estado',
        }
        widgets = {
            'colaborador_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'Tipo_Formato_CartaFK': forms.Select(attrs={'class': 'form-control select2'}),
            'propietario_doc': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_inicio_vacacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin_vacacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dias_vacaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_inicio_alternativa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin_alternativa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dias_alternativo': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'accion_irregular': forms.Textarea(attrs={'class': 'form-control'}),
            'reportes_anexos': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control select2'}),
        }