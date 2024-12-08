from django.db import models

from shared.models.baseModel import BaseModel


# Activo, en reparacion, dañado, dado de baja, en garantia
class Estado_Articulo(BaseModel):
    Id_EstadoArticulo = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250, unique=True)
    Observacion = models.CharField(max_length=1000, blank=True, null=True)
    Activo = models.BooleanField("activo", default= True)#variable activo
    def __str__(self):
        return self.Descripcion
    class Meta:
        verbose_name="EstadoArticulo"
        verbose_name_plural = 'EstadoArticulo'
        ordering = ['Descripcion']