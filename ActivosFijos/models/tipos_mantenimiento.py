from django.db import models

from shared.models.baseModel import BaseModel
#Tabla tipos de mantenimineto (preventivo correctivo  )
class Mantenimineto_Tipos(BaseModel):
    Id_TipoMantenimiento = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250, unique=True)
    Observacion = models. CharField(max_length=400, blank=True, null=True)
    Activo = models.BooleanField("activo", default= True)#variable activo

    def __str__(self):
        return str(self.Descripcion)
    class meta:
        verbose_name ="Tipo_Mantenimiento"
        verbose_name_plural = 'Tipo_Mantenimiento'
        ordering = ['Descripcion']
