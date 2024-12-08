from django import forms
from RrHh.models.contrato_laboral import *
import datetime
now = datetime.datetime.now()

class Contrato_LaboralForm(forms.ModelForm):
    class Meta:
        model = Contrato_Laboral
        fields = [
            'id',
            'hoja_vida_FK',
            'empresa',
            'cargo',
            'fecha_inicio',
            'fecha_inicio_laboral',
            'fecha_fin',
            'tipo_contratoFK',
            'salario',
            'estado_FK',
            ]
        labels = {
            'hoja_vida_FK': 'Hoja de vida',
            'empresa': 'Empresa',
            'cargo': 'Cargo',
            'fecha_inicio': 'Fecha de inicio del contrato',
            'fecha_inicio_laboral': 'Fecha de inicio laboral',
            'fecha_fin': 'Fecha de fin',
            'tipo_contratoFK': 'Tipo de Contrato',
            'salario': 'Sueldo',
            'estado_FK': 'Estado del contrato',
        }
        widgets = {
            'hoja_vida_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'empresa': forms.Select(attrs={'class': 'form-control select2'}),
            'cargo': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_inicio': forms.TextInput(attrs={'type': 'date','value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'fecha_inicio_laboral': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'fecha_fin': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'tipo_contratoFK': forms.Select(attrs={'class': 'form-control select2'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado_FK': forms.Select(attrs={'class': 'form-control select2'}),
        }

class RenunciaForm(forms.ModelForm):
    class Meta:
        model = Contrato_Laboral
        fields = [
            'id',
            'fecha_renuncia',
            'carta_renuncia',
            'motivo_fin_contrato',
            'fecha_notificacion_renuncia',
            ]
        labels = {
            'id': 'Numero de contrato',
            'fecha_renuncia': 'Fecha de Renuncia',
            'carta_renuncia': 'Carta de Renuncia',
            'motivo_fin_contrato': 'Motivo Fin de Contrato',
            'fecha_notificacion_renuncia': 'Fecha de Notificacion Renuncia',
        }
        widgets = {
            'id': forms.NumberInput(attrs={'class': 'form-control '}),
            'fecha_renuncia': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'carta_renuncia': forms.FileInput(attrs={'class': 'form-control '}),
            'motivo_fin_contrato': forms.Textarea(attrs={'class': 'form-control '}),
            'fecha_notificacion_renuncia': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
        }

class DespidoForm(forms.ModelForm):
    class Meta:
        model = Contrato_Laboral
        fields = [
            'fecha_despido',
            'motivo_fin_contrato',
            ]
        labels = {
            'fecha_despido': 'Fecha de Renuncia',
            'motivo_fin_contrato': 'Motivo Fin de Contrato',
        }
        widgets = {
            'fecha_despido': forms.TextInput(attrs={'type': 'date', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'motivo_fin_contrato': forms.Textarea(attrs={'class': 'form-control '}),
        }

class Anexo_ContratoForm(forms.ModelForm):
    class Meta:
        model = soportes_contrato
        fields = [
            'nombre_soporte',
            'soporte',
            
            ]
        labels = {
            
            'soporte': 'Soporte',
            'nombre_soporte': 'Nombre del Soporte',
        }
        widgets = {
            
            'soporte': forms.FileInput(attrs={'class': 'form-control '}),
            'nombre_soporte': forms.TextInput(attrs={'class': 'form-control '}),
        }

        
def number_to_words(num):
    if num == 0:
        return 'cero'

    ones = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve']
    teens = ['diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve']
    tens = ['', '', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']
    thousands = ['', 'mil', 'millones', 'mil millones', 'mil millones de millones', 'mil millones de mil millones', 'mil millones de mil millones de millones']

    if num < 10:
        return ones[num]
    elif num < 20:
        return teens[num - 10]
    elif num < 100:
        return tens[num // 10] + ('' if num % 10 == 0 else ' ' + ones[num % 10])
    elif num < 1000:
        return ones[num // 100] + ' cientos' + ('' if num % 100 == 0 else ' ' + number_to_words(num % 100))
    elif num < 1000000:
        return number_to_words(num // 1000) + ' mil' + ('' if num % 1000 == 0 else ' ' + number_to_words(num % 1000))
    elif num < 1000000000:
        return number_to_words(num // 1000000) + ' millones' + ('' if num % 1000000 == 0 else ' ' + number_to_words(num % 1000000))
    else:
        return number_to_words(num // 1000000000) + ' mil millones' + ('' if num % 1000000000 == 0 else ' ' + number_to_words(num % 1000000000))
