from django import forms
from Produccion.models.Proceso_Produccion import *

class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ['nombre', 'cantidad_disponible', 'unidad_medida', 'descripcion']
        labels = {
            'nombre': 'Nombre',
            'cantidad_disponible': 'Cantidad disponible',
            'unidad_medida': 'Unidades de medida',
            'descripcion': 'Descripción',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = ['nombre', 'proceso_produccion', 'descripcion', 'cantidad_producida', 'unidad_medida', 'precio']
        labels = {
            'nombre': 'Nombre',
            'proceso_produccion': 'Proceso de producción',
            'descripcion': 'Descripción',
            'cantidad_producida': 'Cantidad producida',
            'unidad_medida': 'Unidades de medida',
            'precio': 'Precio',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'proceso_produccion': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'cantidad_producida': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class MovimientoMateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = EntradaSalida
        fields = ['materiaprima', 'tipo', 'cantidad','autorizado_por']
        labels = {
            'materiaprima': 'Materia Prima',
            'tipo': 'Tipo de movimiento',            
            'cantidad': 'Cantidad',
            'autorizado_por': 'Autorizado por',
        }
        widgets = {
            'materiaprima': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'autorizado_por': forms.Select(attrs={'class': 'form-control'}),
        }

class MovimientoProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = EntradaSalida
        fields = ['producto_terminado', 'tipo', 'cantidad','autorizado_por']
        labels = {
            'producto_terminado': 'Producto Terminado',
            'tipo': 'Tipo de movimiento',            
            'cantidad': 'Cantidad',
            'autorizado_por': 'Autorizado por',
        }
        widgets = {
            'producto_terminado': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'autorizado_por': forms.Select(attrs={'class': 'form-control'}),
        }