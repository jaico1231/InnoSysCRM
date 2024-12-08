from django.db import models

from ActivosFijos.models.estado_articulo import Estado_Articulo
from ActivosFijos.models.orden_servicio import Articulos_OrdenServicio
from shared.models.baseModel import BaseModel




# aqui se debe actualizar cualquier novedad con los articulos
class Hoja_Vida_Articulos(BaseModel):
    IdHojaVidaArticulo= models.AutoField( primary_key=True)    
    Articulo_FK =   models.ForeignKey(Articulos_OrdenServicio, on_delete=models.CASCADE, blank=True, null=True, related_name='IdArticulosOrdenServicioFK')
    Novedad = models.TextField(blank=True, null=True)
    Estado = models.ForeignKey(Estado_Articulo, on_delete=models.CASCADE, default=1)
    Actualizacion = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return str(self.Articulo_FK)

    class meta:
        verbose_name ="Hoja_Vida_Articulos"
        verbose_name_plural = 'Hoja_Vida_Articulos'
        ordering = ['IdHojaVidaArticulo']
