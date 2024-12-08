
from django.db import models

class Vivienda(models.Model):
    IdVivienda = models.AutoField(primary_key=True)
    Vivienda = models.CharField(max_length=100)
    def __str__(self):
        return self.Vivienda
    class Meta:
        verbose_name="Vivienda"
        verbose_name_plural = 'Vivienda'
        ordering = ['Vivienda']