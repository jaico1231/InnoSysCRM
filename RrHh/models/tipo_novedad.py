
from django.db import models

class Tipo_Novedad(models.Model):
    IdTipoNovedad = models.AutoField(primary_key=True)
    TipoNovedad = models.CharField(max_length=100)
    def __str__(self):
        return self.TipoNovedad
    class Meta:
        verbose_name="TipoNovedad"
        verbose_name_plural = 'TipoNovedad'
        ordering = ['TipoNovedad']