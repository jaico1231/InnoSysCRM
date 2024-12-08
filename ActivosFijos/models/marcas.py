from django.db import models

from shared.models.baseModel import BaseModel



#esta tabla contiene lass marcas de los articulos que se deben crear
class Marcas(BaseModel):
    Id_marca = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250, unique=True)
    Observacion = models.CharField(max_length=1000, blank=True, null=True)
    Activo = models.BooleanField("activo", default= True)#variable activo
    def __str__(self):
        return self.Descripcion
    class Meta:
        verbose_name="Marca"
        verbose_name_plural = 'Marca'
        ordering = ['Descripcion']
