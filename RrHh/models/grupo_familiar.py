
from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.genero import Sexo
from shared.models.tipo_documento import Tipo_Documento
from RrHh.models.hoja_vida import Hoja_Vida, upload_to_hv

class Grupo_Familiar(BaseModel):
    IdGrupo_Familiar = models.AutoField(primary_key=True)
    empleado_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='grupos_familia', null=True, blank=True)
    parentesco_GF = models.CharField(max_length=50, null=True, blank=True)
    nombre_GF = models.CharField(max_length=100, null=True, blank=True)
    apellido_GF = models.CharField(max_length=100, null=True, blank=True)
    sexo_FK_GF = models.ForeignKey(Sexo, on_delete=models.CASCADE, null=True, blank=True)
    fecha_nacimiento_GF = models.DateField('', null=True, blank=True)
    tipo_documento_GF = models.ForeignKey(Tipo_Documento, on_delete=models.CASCADE, null=True, blank=True)
    numero_identificacion_GF = models.CharField(max_length=50, null=True, blank=True)
    anexo_GF = models.FileField(upload_to=upload_to_hv, null=True, blank=True)
    def __str__(self):
        return f"{self.empleado_FK.numero_identificacion} {self.empleado_FK.nombre} {self.empleado_FK.apellido}"

    class Meta:
        verbose_name="Grupo_Familia"
        verbose_name_plural = 'Grupo_Familia'
        ordering = ['-IdGrupo_Familiar']