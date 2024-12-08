
from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models.hoja_vida import Hoja_Vida

class Retiro_Laboral(BaseModel):
    IdRetiro = models.AutoField(primary_key=True)
    colaborador_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE)
    fecha_retiro = models.DateField()
    motivo_retiro = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    validador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validador_retiro', blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Retiro"
        verbose_name_plural = "Retiros"
        ordering = ['-IdRetiro']

    def __str__(self):
        return self.IdRetiro