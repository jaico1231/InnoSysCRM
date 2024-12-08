
from django.db import models

from shared.models.tipo_usuario import Tipo_Usuario

class Tipo_Formato_Carta(models.Model):
    tipo = models.CharField(max_length=100)
    TipoUsuario_FK = models.ForeignKey(Tipo_Usuario, related_name='tipo_formato_carta', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "Tipo Formato Carta"
        verbose_name_plural = "Tipos Formatos Cartas"
        ordering = ['-id']

