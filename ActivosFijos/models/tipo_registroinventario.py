from django.db import models

from shared.models.baseModel import BaseModel

# Registros de entrada y salida
class TipoRegistroInventario(BaseModel):
    Id_TipoRegistroInventario = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250, unique=True)
    Activo = models.BooleanField("activo", default=True)
   
    
    def __str__(self):
        return self.Descripcion
    class Meta:
        verbose_name="TipoRegistroInventario"
        verbose_name_plural = 'TipoRegistroInventario'
        ordering = ['Descripcion']