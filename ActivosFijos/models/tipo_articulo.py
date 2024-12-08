from django.db import models

from shared.models.baseModel import BaseModel

#Materia prima, activos fijos, producto terminado y otros
class TipoArticulo(BaseModel):
    Id_TipoArticulo = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250, unique=True)
    Observacion = models.CharField(max_length=1000, blank=True, null=True)
    Activo = models.BooleanField("activo", default= True)

    def __str__(self):
        return self.Descripcion
    class Meta:
        verbose_name="TipoArticulo"
        verbose_name_plural = 'TipoArticulo'
        ordering = ['Descripcion']
