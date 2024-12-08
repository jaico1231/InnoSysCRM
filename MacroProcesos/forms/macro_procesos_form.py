from django import forms
from MacroProcesos.models.macroprocesos import *

class Tipo_Personal_Form(forms.ModelForm):
    class Meta:
        model = TipoPersonal
        fields = [
            'TipoPersonal',
            'Observacion',
        ]
        labels = {
            'TipoPersonal': 'Tipo De Personal',
            'Observacion': 'Observacion',
        }
        widgets = {
            'TipoPersonal': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class Macro_Procesos_Form(forms.ModelForm):
    class Meta:
        model = MacroProcesos
        fields = [
            'MacroProcesos',
            'Observacion',
        ]
        labels = {
            'MacroProcesos': 'Macro Procesos',
            'Observacion': 'Observacion',
        }
        widgets = {
            'MacroProcesos': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class Proceso_Form(forms.ModelForm):
    class Meta:
        model = Proceso
        fields = [
            'MacroProcesos_FK',
            'Proceso',
            'Observacion',
        ]
        labels = {
            'MacroProcesos_FK': 'Macro Procesos',
            'Proceso': 'Proceso',
            'Observacion': 'Observacion',
        }
        widgets = {
            'MacroProcesos_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'Proceso': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class Subproceso_Form(forms.ModelForm):
    class Meta:
        model = Subprocesos
        fields = [
            'proceso_FK',
            'SubProceso',
            'dueno',
            'gestorriesgo',
            'Observacion',
        ]
        labels = {
            'proceso_FK': 'Proceso',
            'SubProceso': 'Subproceso',
            'Observacion': 'Observacion',
            'dueno': 'Dueño',
            'gestorriesgo': 'Gestor De Riesgo',
        }
        widgets = {
            'proceso_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'SubProceso': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.Textarea(attrs={'class': 'form-control'}),
            'dueno': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'gestorriesgo': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }

class Seccion_Form(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = [
            'Seccion',
            'Observacion',
        ]
        labels = {
            'Seccion': 'Seccion',
            'Observacion': 'Observacion',
        }
        widgets = {
            'Seccion': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class Cargo_Form(forms.ModelForm):
    class Meta:
        model = Cargo_Macroprocesos
        fields = [
            'subproceso',
            'cargo',
            'tipo_personal_FK',
            'seccion',
            'codigo',
            'Observacion',
        ]
        labels = {
            'subproceso': 'Subproceso',
            'cargo': 'Cargo',
            'tipo_personal_FK': 'Tipo Personal',
            'seccion': 'Seccion',
            'codigo': 'Codigo',
            'Observacion': 'Observacion',
        }
        widgets = {
            'seccion': forms.Select(attrs={'class': 'form-control select2'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_personal_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'subproceso': forms.Select(attrs={'class': 'form-control select2'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'Observacion': forms.Textarea(attrs={'class': 'form-control'}),
        }