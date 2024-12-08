
from django.db import models

class Caja_Compensacion(models.Model):
    IdCaja = models.AutoField(primary_key=True)
    Caja = models.CharField(max_length=100)
    def __str__(self):
        return self.Caja
    class Meta:
        verbose_name="CajaCompensacion"
        verbose_name_plural = 'CajaCompensacion'
        ordering = ['Caja']
