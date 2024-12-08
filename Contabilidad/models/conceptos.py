from django.db import models
from shared.models.baseModel import BaseModel

# Ya no recuerdo para que era esta tabla buscarle uso es distinta a concepto en nomina
class Conceptos(BaseModel):
    id = models.BigAutoField(primary_key=True)
    concepto = models.CharField(max_length=200)
    monto = models.FloatField()
    

    class Meta:
        verbose_name = 'Concepto'
        verbose_name_plural = 'Conceptos'
        ordering = ['-id']

class ConfiguracionHorasExtras(BaseModel):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'ConfiguracionHorasExtras'
        verbose_name_plural = 'ConfiguracionHorasExtras'
        ordering = ['-id']

    def __str__(self):
        return self.nombre
