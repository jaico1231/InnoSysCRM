
from django import forms
from django.conf import settings
from RrHh.models.permiso_laboral import Permiso_Laboral
import datetime
from django.http import request
now = datetime.datetime.now()

class Permiso_Laboral_EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Permiso_Laboral
        fields = [
            
            'fecha_solicitada',
            'tipo_permisoFK',
            'tiempo_solicitado_horas',
            'fundamentacion',
            'fecha_solicitada',
        ]
        labels = {
            
            'fecha_solicitada': 'Fecha Requerida',
            'tipo_permisoFK': 'Tipo de Permiso',
            'tiempo_solicitado_horas': 'Tiempo Solicitado (Horas)',
            'fundamentacion': 'Fundamentación',

        }

        widgets = {
            #agregar hiden a solicitante
            
            'fecha_solicitada': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01', 'class': 'form-control'}),
            'tipo_permisoFK': forms.Select(attrs={'class': 'form-control select2'}),
            'tiempo_solicitado_horas': forms.TextInput(attrs={'class': 'form-control'}),
            'fundamentacion': forms.Textarea(attrs={'class': 'form-control'}),
        }

# class Permiso_Laboral_AutorizarForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  # Obtenemos el usuario de los kwargs
#         super(Permiso_Laboral_AutorizarForm, self).__init__(*args, **kwargs)
#         if user:
#             self.fields['autorizador'].initial = user
#     class Meta:
#         model = Permiso_Laboral
#         fields = [
#             'validador',
#             'fecha_validacion',
#             'otro_permiso',
#             'observaciones',
#             'autorizador',
#             'fecha_autorizacion',
#         ]
#         labels = {
#             'estado_FK': 'Estado',
#             'validador': 'Validador',
#             'fecha_validacion': 'Fecha de Validación',
#             'otro_permiso': 'Permiso Otro',
#             'observaciones': 'Observaciones',
#             'autorizador': 'Autorizador',
#             'fecha_autorizacion': 'Fecha de Autorización',
#         }

#         widgets = {
#             'validador': forms.Select(attrs={'class': 'form-control select2'}),
#             'fecha_validacion': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01', 'class': 'form-control'}),
#             'otro_permiso': forms.TextInput(attrs={'class': 'form-control'}),
#             'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
#             'autorizador': forms.Select(attrs={'class': 'form-control select2'}),
#             'fecha_autorizacion': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01', 'class': 'form-control'}),

#         }

class Permiso_Laboral_AutorizarForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(Permiso_Laboral_AutorizarForm, self).__init__(*args, **kwargs)
    #     self.fields['validador'].initial = self.instance.user

    class Meta:
        model = Permiso_Laboral
        fields = [
            'solicitante_FK',
            'fecha_solicitada',
            'tipo_permisoFK',
            'tiempo_solicitado_horas',
            'fundamentacion',
            'estado_FK',
            'fecha_solicitada',
            # 'validador',
            # 'fecha_validacion',
            # 'otro_permiso',
            'observaciones',
            # 'autorizador',
            # 'fecha_autorizacion',
        ]
        labels = {
            'solicitante_FK': 'Empleado',
            'fecha_solicitada': 'Fecha de Solicitud',
            'tipo_permisoFK': 'Tipo de Permiso',
            'tiempo_solicitado_horas': 'Tiempo Solicitado (Horas)',
            'fundamentacion': 'Fundamentación',
            'estado_FK': 'Estado',
            # 'validador': 'Validador',
            # 'fecha_validacion': 'Fecha de Validación',
            # 'otro_permiso': 'Otro Permiso ',
            'observaciones': 'Observaciones',
            'autorizador': 'Autorizador',
            'fecha_autorizacion': 'Fecha de Autorización',
        }
        widgets = {
            'solicitante_FK': forms.Select(attrs={'class': 'form-control', 'readonly': True }),
            'fecha_solicitada': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01', 'class': 'form-control', 'readonly': True}),
            'tipo_permisoFK': forms.Select(attrs={'class': 'form-control ', 'readonly': True}),
            'tiempo_solicitado_horas': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'fundamentacion': forms.Textarea(attrs={'class': 'form-control', 'blockquote': 'true', 'readonly': True,'style': 'transform: auto;'}),
            'estado_FK': forms.Select(attrs={'class': 'form-control select2'}),
            # 'validador': forms.Select(attrs={'class': 'form-control select2'}),
            # 'fecha_validacion': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            # 'otro_permiso': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'autorizador': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_autorizacion': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        }