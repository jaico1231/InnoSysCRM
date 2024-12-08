
from django.db import models

from shared.models.user import User
from RrHh.models.hoja_vida import Hoja_Vida

class Auxilio_No_Prestacional(models.Model):
    IdAuxilio = models.AutoField(primary_key=True)
    colaborador_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE)
    valor = models.IntegerField()
    dias = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    validador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validador_auxilio', blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Auxilio No Prestacional"
        verbose_name_plural = "Auxilio No Prestacionales"
        ordering = ['-IdAuxilio']

    def __str__(self):
        return self.IdAuxilio