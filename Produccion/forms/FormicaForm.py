from django import forms
from Produccion.models.Proceso_Produccion import *

class FormicaForm(forms.ModelForm):
    class Meta:
        model = Formica
        fields = [
            'descripcion',
            'grupo',
        ]

        labels = {
            'descripcion': 'Formica',
            'grupo': 'Grupo',
        }

        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control select2'}),
        }

class GrupoFormicaForm(forms.ModelForm):
    class Meta:
        model = Grupo_Formica
        fields = [
            'grupo',
        ]

        labels = {
            'grupo': 'Grupo',
        }

        widgets = {
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MedidasForm(forms.ModelForm):
    class Meta:
        model = Medidas
        fields = [
            'medida',
            'Descripcion',
        ]

        labels = {
            'medida': 'Medida',
            'Descripcion': 'Descripción',
        }

        widgets = {
            'medida': forms.TextInput(attrs={'class': 'form-control'}),
            'Descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PrecioSuperficieForm(forms.ModelForm):
    class Meta:
        model = Precio_Superficie
        fields = [
            'Formica_FK',
            'Medida_FK',
            'CFT',
            'CFEF',
            'PD',
        ]

        labels = {
            'Formica_FK': 'Formica',
            'Medida_FK': 'Medida',
            'CFT': 'CFT',
            'CFEF': 'CFEF',
            'PD': 'PD',
        }

        widgets = {
            'Formica_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'Medida_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'CFT': forms.TextInput(attrs={'class': 'form-control'}),
            'CFEF': forms.TextInput(attrs={'class': 'form-control'}),
            'PD': forms.TextInput(attrs={'class': 'form-control'}),
        }
        