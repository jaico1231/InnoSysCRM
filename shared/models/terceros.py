import os

from django.urls import reverse
from shared.models.tipo_documento import Tipo_Documento
from shared.models.user import User
from shared.models.estado import Estado
from shared.models.geografia import *
from shared.models.tipo_anexos import *

#Documentos que se puedan solicitar a algun tercero
# la función Cargar_documentos_path toma el número de documento del tercero y el nombre del archivo para crear la ruta de subida del archivo. La función reemplaza los espacios en blanco y los caracteres especiales en el número de documento, y luego concatena la carpeta "archivos_terceros" con el número de documento y el nombre del archivo.
class Tipo_Tercero(BaseModel):
    descripcion = models.CharField ("Nombre", max_length=150)
    sigla = models.CharField ("sigla", max_length=10)

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = 'Tipo de Tercero'
        verbose_name_plural = 'Tipos de Terceros'
        ordering = ['-id']

def Cargar_imagenes_terceros_path(instance, filename):
    NumeroIdentificacion = instance.NumeroIdentificacion
    NumeroIdentificacion = NumeroIdentificacion.replace(" ", "_").replace("-", "_")
    ext = filename.split('.')[-1]
    return os.path.join('img/Terceros', NumeroIdentificacion, f'{filename}')

#Creacion tabla proveedor y/o contratista
#Añadir asesor y estado telefonos tipo tercero
class Terceros(BaseModel):
    Nombre =     models.CharField ("Nombre", max_length=150)
    Apellido = models.CharField('apellido', blank=True, max_length=150, null=True)
    TipoDocumento = models.ForeignKey(Tipo_Documento, on_delete=models.CASCADE, related_name='tipo_tercero', blank=True, null=True)
    NumeroIdentificacion =          models.CharField ("documento",max_length=20, blank=True, unique=True)
    Direccion =          models.CharField ("direccion", max_length=100, blank=True)
    TelefonoFijo =       models.CharField ("telefono fijo", max_length=16, blank=True)
    TelefonoMovil =      models.CharField ("telefono movil", max_length=16, blank=True)
    Email =              models.EmailField ("email ", max_length=80, blank=True, null=True, unique=True)
    asesor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='Asesor')
    Estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default=1, related_name='estado_tercero')
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE, related_name='pais_tercero', blank=True, null=True)
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE, related_name='departamento_tercero', blank=True, null=True)
    municipio = models.ForeignKey(Municipios, on_delete=models.CASCADE, related_name='municipio_tercero', blank=True, null=True)
    update_img = models.ImageField(upload_to=Cargar_imagenes_terceros_path, blank=True, null=True)
    Tipo_Tercero = models.ForeignKey(Tipo_Tercero, on_delete=models.CASCADE, blank=True, null=True, related_name='tipo_tercero')
    
    def __str__(self):
        return f'{self.NumeroIdentificacion} - {self.Nombre} - {self.Apellido}'
    class meta:
        verbose_name ="Proveedor"
        verbose_name_plural = 'Proveedor'
        db_table = 'Proveedor'
    def get_absolute_url(self):
        return reverse('shared:terceros')


def Cargar_documentos_terceros_path(instance, filename):
    # Obtener el número de documento del tercero
    NumeroIdentificacion = instance.NumeroIdentificacion
    # Reemplazar espacios en blanco por guiones bajos y eliminar caracteres especiales
    NumeroIdentificacion = NumeroIdentificacion.replace(" ", "_").replace("-", "_")
    # Obtener la extensión del archivo
    ext = filename.split('.')[-1]
    # Devolver la ruta de subida del archivo
    return os.path.join('DOCS/terceros', NumeroIdentificacion, f'{filename}')


class AnexosTerceros(BaseModel):
    Tercero = models.ForeignKey(Terceros, on_delete=models.CASCADE)
    TipoAnexo = models.ForeignKey(Tipos_Anexos, on_delete=models.CASCADE)
    Archivo = models.FileField(upload_to=Cargar_documentos_terceros_path, blank=True, null=True)

    @property
    def __str__(self):
        return id

    class meta:
        verbose_name ="Anexo Tercero"
        verbose_name_plural = 'Anexos Terceros'
        ordering = ['Tercero']
