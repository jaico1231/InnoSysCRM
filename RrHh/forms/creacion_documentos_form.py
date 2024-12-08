from django import forms
from RrHh.models.creacion_documentos import Creacion_Documentos

class Creacion_DocumentosForm(forms.ModelForm):
    class Meta:
        model = Creacion_Documentos
        fields = [
            'IdDocumentos',
            'colaborador_FK',
            'Tipo_Formato_CartaFK',
            'propietario_doc',
            
        ]
        labels = {
            'IdDocumentos': 'IdDocumentos',
            'colaborador_FK': 'Colaborador',
            'Tipo_Formato_CartaFK': 'Tipo de formato',
            'propietario_doc': 'Propietario',
            
        }
        widgets = {
            'IdDocumentos': forms.TextInput(attrs={'class': 'form-control'}),
            'colaborador_FK': forms.Select(attrs={'class': 'form-control select2'}),
            'Tipo_Formato_CartaFK': forms.Select(attrs={'class': 'form-control select2'}),
            'propietario_doc': forms.Select(attrs={'class': 'form-control select2'}),
            
        }   