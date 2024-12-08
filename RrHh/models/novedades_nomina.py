
from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models.hoja_vida import Hoja_Vida
from RrHh.models.tipo_novedad import Tipo_Novedad
class Novedades_Nomina(BaseModel):
    IdNovedad = models.AutoField(primary_key=True)
    colaborador_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_novedadFK = models.ForeignKey(Tipo_Novedad, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    validador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validador_novedades', blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Novedad Nomina"
        verbose_name_plural = "Novedades Nomina"
        ordering = ['-IdNovedad']

    def __str__(self):
        return self.IdNovedad