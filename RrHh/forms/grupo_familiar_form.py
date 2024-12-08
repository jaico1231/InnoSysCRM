from django import forms
from RrHh.models.grupo_familiar import Grupo_Familiar
import datetime
now = datetime.datetime.now()
class Grupo_FamiliarForm(forms.ModelForm):
    class Meta:
        model = Grupo_Familiar
        fields = [            
            'empleado_FK',
            'parentesco_GF',
            'nombre_GF',
            'apellido_GF',
            'sexo_FK_GF',
            'fecha_nacimiento_GF',
            'tipo_documento_GF',
            'numero_identificacion_GF',
            'anexo_GF',
            ]
        labels = {
            'empleado_FK': 'Empleado',
            'parentesco_GF': 'Parentesco',
            'nombre_GF': 'Nombre de familiar',
            'apellido_GF': 'Apellido de familiar',
            'sexo_FK_GF': 'Genero',
            'fecha_nacimiento_GF': 'Fecha de nacimiento',
            'tipo_documento_GF': 'Tipo de Documento',
            'numero_identificacion_GF': 'Numero de identificación del familiar',
            'anexo_GF': 'Anexo',
        }
        widgets = {
            'empleado_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'parentesco_GF': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_GF': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_GF': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo_FK_GF': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_nacimiento_GF': forms.DateInput(attrs={'type': 'date', 'id': 'start', 'name': 'trip-start', 'value': str(now), 'min': '1900-01-01',  'class': 'form-control '}),
            'tipo_documento_GF': forms.Select(attrs={'class': 'form-control select2'}),
            'numero_identificacion_GF': forms.TextInput(attrs={'class': 'form-control'}),
            'anexo_GF': forms.TextInput(attrs={'class': 'form-control'}),
            }

# if self.request.method == 'POST':
#             grupo_familiar_form = Grupo_FamiliarForm(self.request.POST, self.request.FILES)
#             educacion_form = EducacionForm(self.request.POST, self.request.FILES)
#             experiencia_form = ExperienciaForm(self.request.POST, self.request.FILES)
            
#             if grupo_familiar_form.is_valid():
#                 # valida si el campo nombre tiene datos en el form
#                 if grupo_familiar_form.cleaned_data['nombre_GF'] != '':                
#                     grupo_familiar_form = form.save(commit=False)                    
#                     grupo_familiar_form.empleado_FK_id = self.object.pk
#                     grupo_familiar_form.save()
#                 else:
#                     print('no hay datos')
#                     pass