from django.db import models
from shared.models.baseModel import BaseModel


#Tabla de ingreso de periodos de mantenimiento
class Periocidades(BaseModel):
    Descripcion = models.CharField(max_length=250, unique=True)
    Observacion = models. CharField(max_length=400, blank=True, null=True)
    CantidadDias = models.IntegerField()
    Meses = models.IntegerField()

    
    def __str__(self):
        return str(self.Descripcion)
    class meta:
        verbose_name ="Periocidades"
        verbose_name_plural = 'Periocidades'
        ordering = ['Descripcion']
