from django import forms
from shared.models.datos_empresa import DatosIniciales

class DatosInicialesForm(forms.ModelForm):
    class Meta:
        model = DatosIniciales
        fields = ['nombre',
                  'nit',
                  'logo',
                  'reprelegal',
                  'tipodoc',
                  'documento_representante',
                  'cargo',
                  'periocidadpago',
                  'pais',
                  'Departamento',
                  'municipio',
                  'numerocuenta',
                  'banco',
                  'tipocuenta',
                  'correo',
                  'telefono',
                  'direccion']
        
        labels = {
            'nombre': 'Nombre de la Empresa',
            'nit': 'NIT de la Empresa',
            'logo': 'Logo de la Empresa',
            'reprelegal': 'Representante Legal',
            'tipodoc': 'Tipo de Documento',
            'documento_representante': 'Documento del Representante',
            'cargo': 'Cargo del Representante',
            'periocidadpago': 'Periocidad de Pago',
            'pais': 'Pais',
            'Departamento': 'Departamento',
            'municipio': 'Municipio',
            'numerocuenta': 'Numero de Cuenta',
            'banco': 'Banco',
            'tipocuenta': 'Tipo de Cuenta',
            'correo': 'Correo de la Empresa',
            'telefono': 'Telefono de la Empresa',
            'direccion': 'Direccion de la Empresa',

        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'reprelegal': forms.TextInput(attrs={'class': 'form-control'}),
            'tipodoc': forms.Select(attrs={'class': 'form-control'}),
            'documento_representante': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'periocidadpago': forms.Select(attrs={'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
            'Departamento': forms.Select(attrs={'class': 'form-control'}),
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'numerocuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'tipocuenta': forms.Select(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),

        }
