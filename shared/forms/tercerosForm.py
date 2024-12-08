from django import forms
from shared.models.terceros import AnexosTerceros, Terceros


class TercerosForm(forms.ModelForm):
    class Meta:
        model = Terceros
        fields = [
            'Nombre', 
            'Apellido', 
            'TipoDocumento', 
            'NumeroIdentificacion', 
            'Direccion',
            'TelefonoFijo', 
            'TelefonoMovil', 
            'Email', 
            # 'asesor',
            'pais',
            'municipio',
            'departamento',
            'update_img',
            # 'Tipo_Tercero',
            
            ]
            
        labels = {
            'Nombre': 'Nombre o Razón Social',
            'Apellido': 'Apellido',
            'TipoDocumento': 'Tipo de Documento',
            'NumeroIdentificacion': 'Documento',
            'Direccion': 'Dirección',
            'TelefonoFijo': 'Telefono Fijo',
            'TelefonoMovil': 'Telefono Movil',
            'Email': 'Email',
            # # 'asesor': 'Asesor',
            'pais': 'Pais',
            'municipio': 'Municipio',
            'departamento': 'Departamento',
            'update_img': 'Imagen',
            # 'Tipo_Tercero': 'Tipo de Tercero',
        }

        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'TipoDocumento': forms.Select(attrs={'class': 'form-control select2'}),
            'NumeroIdentificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'TelefonoFijo': forms.TextInput(attrs={'class': 'form-control'}),
            'TelefonoMovil': forms.TextInput(attrs={'class': 'form-control'}),
            'Email': forms.TextInput(attrs={'class': 'form-control'}),
            # 'asesor': forms.Select(attrs={'class': 'form-control select2'}),
            'pais': forms.Select(attrs={'class': 'form-control select2'}),
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'update_img': forms.FileInput(attrs={'class': 'form-control'}),
            # 'Tipo_Tercero': forms.Select(attrs={'class': 'form-control select2'}),
        }
class AnexoTercerosForm(forms.ModelForm):
    class Meta:
        model = AnexosTerceros
        fields = [
            'Tercero',
            'TipoAnexo',
            'Archivo',
        ]

        labels = {
            'Tercero': 'Terceros',
            'TipoAnexo_FK': 'Tipo Anexo',
            'Archivo': 'Elija un archivo',
        }
        widgets = {
            'Tercero': forms.Select(attrs={'class': 'form-control select2'}),
            'TipoAnexo': forms.Select(attrs={'class': 'form-control select2'}),
            'Archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }