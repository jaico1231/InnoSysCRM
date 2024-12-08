
from django.db import models

class Tipo_Retiro_Cesantias(models.Model):
    IdTipoRetiroCesantias = models.AutoField(primary_key=True)
    TipoRetiroCesantias = models.CharField(max_length=100)
    def __str__(self):
        return self.TipoRetiroCesantias
    class Meta:
        verbose_name="TipoRetiroCesantias"
        verbose_name_plural = 'TipoRetiroCesantias'
        ordering = ['TipoRetiroCesantias']
