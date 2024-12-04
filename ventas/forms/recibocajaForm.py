from datetime import datetime
from django import forms
from shared.models.terceros import Terceros

from ventas.models.ventas import CuentaPorCobrar, ReciboCaja, Venta
from django.db.models import Sum, F
from django.utils.timezone import now

class ReciboCajaForm(forms.ModelForm):
    saldo_pendiente = forms.DecimalField(
        label='Saldo pendiente', 
        max_digits=50, 
        decimal_places=2, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly', 'id': 'saldo-pendiente'})
    )
    
    class Meta:
        model = ReciboCaja        
        fields = ['fecha','cuenta_por_cobrar','metodo_pago', 'total', 'observaciones']
        labels = {
            'cuenta_por_cobrar': 'Factura a Pagar',
        }
        widgets = {
            'cuenta_por_cobrar': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ReciboCajaForm, self).__init__(*args, **kwargs)
        self.fields['cuenta_por_cobrar'].queryset = CuentaPorCobrar.objects.filter(saldo_pendiente__gt=0)
                
        if 'fecha' not in self.initial:
            self.initial['fecha'] = now().strftime('%Y-%m-%d')
            self.fields['fecha'].widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'date','colspan': 1})

            
# class ReciboCajaForm(forms.ModelForm):
#     saldo_pendiente = forms.DecimalField(
#         label='Saldo pendiente', 
#         max_digits=50, 
#         decimal_places=2, 
#         required=False, 
#         widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly', 'id': 'saldo-pendiente'})
#     )
#     class Meta:
#         model = ReciboCaja        
#         fields = ['fecha','cuenta_por_cobrar','metodo_pago', 'total', 'observaciones']
#         labels = {
#             'cuenta_por_cobrar': 'Factura a Pagar',
#         }
#         widgets = {
#             'cuenta_por_cobrar': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
#             'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
#             'total': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
#             'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            
#         }

#     # Opcional: Añadir widgets para mejorar la presentación del formulario
#     def __init__(self, *args, **kwargs):
#         super(ReciboCajaForm, self).__init__(*args, **kwargs)
#         self.fields['cuenta_por_cobrar'].queryset = CuentaPorCobrar.objects.filter(saldo_pendiente__gt=0)
                
#         if 'fecha' not in self.initial:
#             self.initial['fecha'] = now().strftime('%Y-%m-%d')
#             self.fields['fecha'].widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'date','colspan': 1})

    # def __init__(self, *args, **kwargs):
    #     super(ReciboCajaForm, self).__init__(*args, **kwargs)
    #     if 'fecha' not in self.initial:
    #         self.initial['fecha'] = now.strftime('%Y-%m-%d')
    #     self.fields['fecha'].widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    # #     if 'tercero' in self.data:
    # #         try:
    #             tercero_id = int(self.data.get('tercero'))
    #             self.fields['ventas'].queryset = Venta.objects.filter(
    #                 tercero_id=tercero_id
    #             ).filter(
    #                 total__gt=F('recibos_caja_ventas__total')  # Filtra las ventas con saldo pendiente
    #             )
    #         except (ValueError, TypeError):
    #             self.fields['ventas'].queryset = Venta.objects.none()
    #     elif self.instance.pk:
    #         self.fields['ventas'].queryset = self.instance.tercero.ventas.filter(
    #             total__gt=F('recibos_caja_ventas__total')
    #         )

# class ReciboCajaForm(forms.ModelForm):
#     saldo_pendiente = forms.DecimalField(
#         label='Saldo pendiente', 
#         max_digits=50, 
#         decimal_places=2, 
#         required=False, 
#         widget=forms.TextInput(attrs={
#             'class': 'form-control', 
#             'readonly': 'readonly', 
#             'id': 'saldo-pendiente'
#         })
#     )

#     class Meta:
#         model = ReciboCaja
#         fields = ['fecha', 'cuenta_por_cobrar', 'metodo_pago', 'total', 'observaciones']
#         widgets = {
#             'cuenta_por_cobrar': forms.Select(attrs={'class': 'form-control select2'}),
#             'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
#             'total': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
#             'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'fecha': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
#         }

#     def __init__(self, *args, **kwargs):
#         super(ReciboCajaForm, self).__init__(*args, **kwargs)
        
#         # Filtrar las cuentas por cobrar con saldo pendiente
#         self.fields['cuenta_por_cobrar'].queryset = CuentaPorCobrar.objects.filter(saldo_pendiente__gt=0)

#         # Establecer la fecha inicial si no se ha proporcionado
#         if not self.initial.get('fecha'):
#             self.initial['fecha'] = now().strftime('%Y-%m-%d')



class ReciboCaja2Form(forms.ModelForm):
    tercero = forms.ModelChoiceField(
        queryset=Terceros.objects.all(), 
        required=True, 
        label="Cliente", 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    ventas = forms.ModelMultipleChoiceField(
        queryset=Venta.objects.none(),  # Se llenará dinámicamente
        required=True, 
        label="Ventas con saldo pendiente",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = ReciboCaja
        fields = ['tercero', 'ventas', 'fecha', 'metodo_pago', 'tipo_transaccion', 'total', 'observaciones']
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'tipo_transaccion': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ReciboCajaForm, self).__init__(*args, **kwargs)
        if 'fecha' not in self.initial:
            self.initial['fecha'] = now.strftime('%Y-%m-%d')
        self.fields['fecha'].widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    
    
    
    
    #     if 'tercero' in self.data:
    #         try:
    #             tercero_id = int(self.data.get('tercero'))
    #             self.fields['ventas'].queryset = Venta.objects.filter(
    #                 tercero_id=tercero_id
    #             ).filter(
    #                 total__gt=F('recibos_caja_ventas__total')  # Filtra las ventas con saldo pendiente
    #             )
    #         except (ValueError, TypeError):
    #             self.fields['ventas'].queryset = Venta.objects.none()
    #     elif self.instance.pk:
    #         self.fields['ventas'].queryset = self.instance.tercero.ventas.filter(
    #             total__gt=F('recibos_caja_ventas__total')
    #         )
