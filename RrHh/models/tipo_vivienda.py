
from django.db import models
class Tipo_Vivienda(models.Model):
    IdTipoVivienda = models.AutoField(primary_key=True)
    TipoVivienda = models.CharField(max_length=100)
    def __str__(self):
        return self.TipoVivienda
    class Meta:
        verbose_name="TipoVivienda"
        verbose_name_plural = 'TipoVivienda'
        ordering = ['TipoVivienda']
