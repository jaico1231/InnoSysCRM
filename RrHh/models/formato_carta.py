
from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models.tipo_formato_carta import Tipo_Formato_Carta
class Formato_Carta(BaseModel):
    tipo_formato_FK = models.ForeignKey(Tipo_Formato_Carta, on_delete=models.CASCADE, blank=True, null=True)
    nombre_formato = models.CharField(max_length=100, blank=True, null=True)
    codigo_formato = models.CharField(max_length=100,blank=True, null=True)
    version = models.CharField(max_length=100,blank=True, null=True)
    fecha_creacion = models.DateField()
    fecha_aprobacion = models.DateField('fecha de aprobacion',blank=True, null=True)
    elaborado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formatos_elaborados',blank=True, null=True)
    aprobaado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formatos_aprobados',blank=True, null=True)
    divulgacion = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.codigo_formato

    class Meta:
        verbose_name = "Formato Carta"
        verbose_name_plural = "Formatos Cartas"
        ordering = ['-id']