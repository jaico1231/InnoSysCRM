
from django.db import models

from shared.models.baseModel import BaseModel
from RrHh.models.hoja_vida import Hoja_Vida

class experiencia_laboral(BaseModel):
    IdExperiencia_Laboral = models.AutoField(primary_key=True)
    hoja_vida_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='experiencia_laboral', null=True, blank=True)
    cargo_EXP = models.CharField(max_length=100, null=True, blank=True)
    empresa_EXP = models.CharField(max_length=100, null=True, blank=True)
    fecha_inicio_EXP = models.DateField(null=True, blank=True)
    fecha_fin_EXP = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.IdExperiencia_Laboral} "

    class Meta:
        verbose_name="Experiencia_Laboral"
        verbose_name_plural = 'Experiencia_Laboral'
        ordering = ['-IdExperiencia_Laboral']
