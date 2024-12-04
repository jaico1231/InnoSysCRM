from django.db import models

class Sexo(models.Model):
    Descripcion = models.CharField(max_length=250)
    def __str__(self):
        return self.Descripcion
    class Meta:
        verbose_name="Sexo"
        verbose_name_plural = 'Sexo'
        ordering = ['Descripcion']