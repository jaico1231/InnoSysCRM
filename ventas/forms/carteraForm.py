# forms.py

from django import forms

from configuracion.models.servicios import Medicos
from shared.models.terceros import Terceros


class CarteraTerceroForm(forms.Form):
    tercero = forms.ModelChoiceField(
        queryset=Medicos.objects.all(),
        required=False, 
        label="Seleccionar Medico",
        widget=forms.Select(attrs={'class': 'form-control select2'})
        )
    fecha_inicio = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}), label="Fecha Inicio")
    fecha_fin = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}), label="Fecha Fin")

