from django import forms
from django.urls import reverse_lazy
from ActivosFijos.models.cronograma import CronogramaMantenimiento, BitacoraMantenimiento

class CronogramaMantenimientoForm(forms.ModelForm):
    class Meta:
        model = CronogramaMantenimiento
        fields = [
            'catArticulo',
            'fecha_programada',
            'tipo_mantenimiento',
            'descripcion',
            'tercero',
            'periocidad',
        ]
        labels = {
            'catArticulo': 'Grupo',
            'fecha_programada': 'Fecha Programada',
            'tipo_mantenimiento': 'Tipo de Mantenimiento',
            'descripcion': 'Descripción',
            'tercero': 'Tercero/prveedor',
            'periocidad': 'Periocidad',
        }

        widgets = {
            'catArticulo': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_programada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_mantenimiento': forms.Select(attrs={'class': 'form-control select2'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'tercero' : forms.Select(attrs={'class': 'form-control select2'}),
            # 'tercero': forms.Select(attrs={'class': 'form-control select2 with-add-button', 'data-url': reverse_lazy('administracion:create_tercero')}),
            'periocidad': forms.Select(attrs={'class': 'form-control select2'}),
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Agregar el botón "+" junto a cada campo Select
    #     for field in ['catArticulo', 'tipo_mantenimiento', 'tercero', 'periocidad']:
    #         url_name = f'ACTIVOS:create_{field}'  # Supongamos que tienes una URL de creación para cada modelo
    #         url = reverse_lazy(url_name)
    #         self.fields[field].widget.attrs['class'] += ' with-add-button'
    #         self.fields[field].widget.attrs['data-url'] = url

class BitacoraMantenimientoForm(forms.ModelForm):
    class Meta:
        model = BitacoraMantenimiento
        fields = [
            'articulo',
            'fecha_realizacion',
            'observaciones',
            'documentos',
            'Novedad',
            'orden_servicio',
            'tipomantenimiento',
            'Estado',
            'Actualizacion',
            'documentos'
        ]
        labels = {
            'articulo': 'Articulo',
            'fecha_realizacion': 'Fecha Realización',
            'observaciones': 'Observaciones',
            'documentos': 'Documentos',
            'Novedad': 'Novedad',
            'orden_servicio': 'Orden de Servicio',
            'tipomantenimiento': 'Tipo de Mantenimiento',
            'Estado': 'Estado',
            'Actualizacion': 'Actualizacion',
        }

        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_realizacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control'}),
            'documentos': forms.FileInput(attrs={'class': 'form-control'}),
            'Novedad': forms.TextInput(attrs={'class': 'form-control'}),
            'orden_servicio': forms.Select(attrs={'class': 'form-control select2'}),
            'tipomantenimiento': forms.Select(attrs={'class': 'form-control select2'}),
            'Estado': forms.Select(attrs={'class': 'form-control select2'}),
            'Actualizacion': forms.TextInput(attrs={'class': 'form-control'}),
        }