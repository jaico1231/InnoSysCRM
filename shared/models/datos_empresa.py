from django.db import models
import re
from shared.models.tipo_cuenta import Tipo_Cuenta
from shared.changelogo import update_base_html
from shared.models.geografia import Paises, Departamentos, Municipios
from shared.models.tipo_documento import Tipo_Documento
from shared.models.periocidades import Periocidades
from shared.models.baseModel import BaseModel

def Logo_Empresa_path(instance, filename):
    # Obtener el número de documento del tercero
    identificacion = instance.NumeroIdentificacion
    # Reemplazar espacios en blanco por guiones bajos y eliminar caracteres especiales
    identificacion = re.sub(r'\W+', '_', str(identificacion))
    # Obtener la extensión del archivo
    ext = filename.split('.')[-1]
    # Devolver la ruta de subida del archivo
    return f'img/logos/{identificacion}/{filename}'

class DatosIniciales(BaseModel):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=100, null=True, blank=True) # models.IntegerField()
    direccion = models.CharField(max_length=100,null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)
    reprelegal = models.CharField(max_length=100, null=True, blank=True)
    tipodoc= models.ForeignKey(Tipo_Documento, on_delete=models.CASCADE, null=True, blank=True)
    documento_representante = models.IntegerField(null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    periocidadpago = models.ForeignKey(Periocidades, on_delete=models.CASCADE, null=True, blank=True)
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE, null=True, blank=True)
    Departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE, null=True, blank=True)
    municipio = models.ForeignKey(Municipios, on_delete=models.CASCADE, null=True, blank=True)
    numerocuenta = models.CharField(max_length=100, null=True, blank=True)
    banco = models.CharField(max_length=100, null=True, blank=True)
    tipocuenta = models.ForeignKey(Tipo_Cuenta, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(upload_to=Logo_Empresa_path, verbose_name='Logo de La Empresa', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(DatosIniciales, self).save(*args, **kwargs)
        # Actualizar el archivo base.html con el nuevo logo
        update_base_html(self.logo.url if self.logo else None)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Datos de la Empresa"
        verbose_name_plural = 'Datos de la Empresa'
        ordering = ['nombre']