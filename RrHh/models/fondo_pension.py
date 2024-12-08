
from django.db import models

class fondo_pension(models.Model):
    fondo = models.CharField(max_length=100)
    def __str__(self):
        return self.fondo
    class Meta:
        verbose_name="fondo_pension"
        verbose_name_plural = 'fondo_pension'
        ordering = ['fondo']

