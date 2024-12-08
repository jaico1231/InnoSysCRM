
from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models.hoja_vida import Hoja_Vida

class RodamientoNoPrestacional(BaseModel):
    IdRodamiento = models.AutoField(primary_key=True)
    colaborador_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE)
    valor = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    validador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validador_rodamiento', blank=True, null=True)
    

    class Meta:
        verbose_name = "Rodamiento No Prestacional"
        verbose_name_plural = "Rodamiento No Prestacionales"
        ordering = ['-IdRodamiento']

    def __str__(self):
        return self.IdRodamiento