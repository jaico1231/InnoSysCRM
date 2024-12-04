from django.db import models

class Tipo_Cuenta(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = "Tipo de Cuenta"
        verbose_name_plural = 'Tipos de Cuenta'
        ordering = ['nombre']