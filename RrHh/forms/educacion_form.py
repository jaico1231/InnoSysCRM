from django import forms
from RrHh.models.educacion import Educacion
import datetime
now = datetime.datetime.now()
class EducacionForm(forms.ModelForm):
    class Meta:
        model = Educacion
        fields = [
            
            'hoja_vida_FK',
            'institucion_EDU',
            'titulo_EDU',
            'pais_EDU',
            'duracion_EDU',
            'TextoUnidad_EDU',
            'fecha_inicio_EDU',
            'fecha_fin_EDU',
            'upload_docs_EDU',
            ]
        labels = {
            'hoja_vida_FK': 'Empleado',
            'institucion_EDU': 'Institución',
            'titulo_EDU': 'Titulo',
            'pais_EDU': 'Pais',
            'duracion_EDU': 'Duración',
            'TextoUnidad_EDU': 'Unidad',
            'fecha_inicio_EDU': 'Fecha de inicio',
            'fecha_fin_EDU': 'Fecha de fin',
            'upload_docs_EDU': 'Cargar documento',
        }
        widgets = {
            'hoja_vida_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'institucion_EDU': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_EDU': forms.TextInput(attrs={'class': 'form-control'}),
            'pais_EDU': forms.Select(attrs={'class': 'form-control select2'}),
            'duracion_EDU': forms.TextInput(attrs={'class': 'form-control'}),
            'TextoUnidad_EDU': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio_EDU': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'fecha_fin_EDU': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'upload_docs_EDU': forms.FileInput(attrs={'class': 'form-control'}),
            }

