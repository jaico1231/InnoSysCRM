from django.db import models
from shared.models.baseModel import BaseModel


class TipoPago(BaseModel):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Pago"
        verbose_name_plural = 'Tipos de Pago'
        ordering = ['nombre']

class TipoTransaccion(BaseModel):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre