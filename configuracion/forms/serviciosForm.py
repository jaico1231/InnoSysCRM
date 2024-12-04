from django import forms
from configuracion.models.servicios import Servicios, Paquetes, PaquetesServicios, Medicos, Medico_paquetes 

class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = [
            'nombre',
            'descripcion',
            'codigo',
            'precio',
        ]

        labels = {
            'nombre': 'Servicio',
            'descripcion': 'Descripción', 
            'estado': 'Activo',
            'codigo': 'Código',
            'precio': 'Precio',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion':  forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class PaquetesForm(forms.ModelForm):
    class Meta:
        model = Paquetes
        fields = [
            'nombre',
            
            'precio',
        ]

        labels = {
            'nombre': 'Paquete',
            'estado': 'Estado',
            'precio': 'Precio',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PaquetesServiciosForm(forms.ModelForm):
    servicios = forms.ModelMultipleChoiceField(
        queryset=Servicios.objects.filter(estado=True),  # Solo los servicios activos
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select selectpicker', 
            'data-live-search': 'true',
            'title': 'Seleccione los servicios'
        }),
        required=False
    )

    class Meta:
        model = Paquetes
        fields = ['nombre', 'codigo',  'servicios']

        labels = {
            'nombre': 'Paquete',
            'codigo': 'Código Paquete',
            'servicios': 'Servicios del Paquete',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PaquetesUpdateForm(forms.ModelForm):
    servicios = forms.ModelMultipleChoiceField(
        queryset=Servicios.objects.filter(estado=True),  # Solo los servicios activos
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control selectpicker', 
            'data-live-search': 'true',
            'title': 'Seleccione los servicios'
        }),
        required=False
    )

    class Meta:
        model = Paquetes
        fields = ['nombre', 'codigo', 'precio', 'servicios']

        labels = {
            'nombre': 'Paquete',
            'codigo': 'Código Paquete',
            'precio': 'Precio',
            'servicios': 'Servicios del Paquete',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MedicosForm(forms.ModelForm):
    paquetes = forms.ModelMultipleChoiceField(
        queryset=Paquetes.objects.filter(estado=True),  # Solo los paquetes activos
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select selectpicker', 
            'data-live-search': 'true',
            'title': 'Seleccione los paquetes'
        }),
        required=False
    )
    class Meta:
        model = Medicos
        fields = [
            'tercero',
            'comision',
            'descuento',
        ]

        labels = {
            'tercero': 'Medico',
            'comision': 'Comision',
            'descuento': 'Descuento',
        }

        widgets = {
            'tercero': forms.Select(attrs={'class': 'form-control'}),
            'comision': forms.NumberInput(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class Medico_paquetesForm(forms.ModelForm):
    class Meta:
        model = Medico_paquetes
        fields = [
            'medico',
            'paquete',
        ]

        labels = {
            'medico': 'Medico',
            'paquete': 'Paquete',
        }

        widgets = {
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'paquete': forms.Select(attrs={'class': 'form-control'}),
        }