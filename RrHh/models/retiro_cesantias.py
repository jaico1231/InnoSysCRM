
from django.db import models
import re

from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models.hoja_vida import Hoja_Vida

def upload_to_cesantias(instance, filename):
    # Obtener el número de documento del tercero
    numero_identificacion = instance.numero_identificacion
    # Reemplazar espacios en blanco por guiones bajos y eliminar caracteres especiales
    numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
    # Obtener la extensión del archivo
    ext = filename.split('.')[-1]
    # Devolver la ruta de subida del archivo
    # return os.path.join('archivos_terceros', IdArticulo, f'{instance.IdArticuloFK.IdArticulo}/{filename}')
    return f'DOCUMENTOS/{numero_identificacion}/CESANTIAS/{filename}'

class Retiro_Cesantias(BaseModel):
    IdRetiroCesantias = models.AutoField(primary_key=True)
    colaborador_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE)
    fecha_retiro = models.DateField()
    motivo_retiro = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    validador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validador_retiro_cesantias', blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    File = models.FileField(upload_to=upload_to_cesantias, blank=True, null=True)

    class Meta:
        verbose_name = "Retiro Cesantias"
        verbose_name_plural = "Retiros Cesantias"
        ordering = ['-IdRetiroCesantias']

    def __str__(self):
        return self.IdRetiroCesantias