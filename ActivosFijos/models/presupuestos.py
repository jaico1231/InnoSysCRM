from django.db import models

from shared.models.baseModel import BaseModel

class Presupuestos(BaseModel):
    Id_Presupuesto = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250)
    Observacion = models. CharField(max_length=400, blank=True, null=True)
    cantidad = models.IntegerField()
    Activo = models.BooleanField("activo", default= True)#variable activo
    Fecha_Aprobacion = models.DateTimeField('fecha creación', blank=True, null=True)
    Fecha_cierre = models.DateTimeField('fecha Cierre', blank=True, null=True)
    
    def __str__(self):
        return str(self.Descripcion)
    class meta:
        verbose_name ="Presupuesto"
        verbose_name_plural = 'Presupuesto'
        ordering = ['Descripcion']
