
from django.db import models

    # "Contrato por obra o labor",
    # "Contrato de trabajo a término fijo",
    # "Contrato de trabajo a término indefinido",
    # "Contrato de aprendizaje",
    # "Contrato temporal, ocasional o accidental",
class tipo_contrato(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):  
        return self.tipo

    class Meta:
        verbose_name="tipo_contrato"
        verbose_name_plural = 'tipo_contrato'
        ordering = ['tipo']
   