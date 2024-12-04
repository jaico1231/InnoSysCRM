

from django import forms
from ventas.models.ventas import CuentaPorCobrar


class CuentaxCobrarForm(forms.ModelForm):
    class Meta:
        model = CuentaPorCobrar
        fields = ['venta', 'total_cobrado', 'observaciones']
        labels = {
            'venta': 'Factura',
            'medico': 'Medico',
            'fecha_vencimiento': 'Fecha Vencimiento',
            'saldo_pendiente': 'Saldo Pendiente',
            'total_cobrado': 'Total Cobrado',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'venta': forms.Select(attrs={'class': 'form-control select2'}),
            'medico': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_vencimiento': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'saldo_pendiente': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_cobrado': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }
