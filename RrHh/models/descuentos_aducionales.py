
from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models.hoja_vida import Hoja_Vida

class Descuentos_Adicionales(BaseModel):
    IdDescuentos = models.AutoField(primary_key=True)
    colaborador_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE)
    valor = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    validador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validador_descuentos', blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Descuentos Adicionales"
        verbose_name_plural = "Descuentos Adicionales"
        ordering = ['-IdDescuentos']

    def __str__(self):
        return self.IdDescuentos