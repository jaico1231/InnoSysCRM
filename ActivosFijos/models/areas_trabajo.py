from django.db import models

from shared.models.baseModel import BaseModel

#Creacion de tabla para las areas de trabajo
class Areas_Trabajo(BaseModel):
    Id_Area =  models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250)
    Observacion = models. CharField(max_length=400, blank=True, null=True)
    Activo = models.BooleanField("activo", default= True)#variable activo
    
    def __str__(self):
        return str(self.Descripcion)
    class meta:
        verbose_name ="Area"
        verbose_name_plural = 'Area'
        ordering = ['Descripcion']
