from django import forms
from Contabilidad.models.retroactivo import RodamNoPresta, DatosFinancierosEmpleado, AuxilioNoPrestacional,DescuentoAdicional, CampoAdicionalLiquidacion,Tabla_Precios_Rutas, RutaVisitas
from Contabilidad.models.nomina import *


class UploadCSVForm(forms.Form):
    file = forms.FileField(
        label='Selecciona un archivo CSV',
        help_text='Máximo 42 MB'
    )
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('El archivo no es un CSV válido.')
        if file.size > 42 * 1024 * 1024:
            raise forms.ValidationError('El archivo es demasiado grande (máximo 42 MB).')
        return file
    

class NovedadNominaForm(forms.ModelForm):
    class Meta:
        model = NovedadNomina
        fields = '__all__'

class ConfiguracionNominaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionNomina
        fields = '__all__'

class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = '__all__'

class DatosFinancierosEmpleadoForm(forms.ModelForm):
    class Meta:
        model = DatosFinancierosEmpleado
        fields = '__all__'

class AuxilioNoPrestacionalForm(forms.ModelForm):
    class Meta:
        model = AuxilioNoPrestacional
        fields = '__all__'

class RodamientoNoPrestacionalForm(forms.ModelForm):
    class Meta:
        model = RodamNoPresta
        fields = '__all__'

class DescuentoAdicionalForm(forms.ModelForm):
    class Meta:
        model = DescuentoAdicional
        fields = '__all__'

class CampoAdicionalLiquidacionForm(forms.ModelForm):
    class Meta:
        model = CampoAdicionalLiquidacion
        fields = '__all__'
