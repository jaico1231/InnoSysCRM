import re
from django.db import models
from ActivosFijos.models.articulos import Articulo
from ActivosFijos.models.categoria_articulos import Categoria_Articulo
from ActivosFijos.models.estado_articulo import Estado_Articulo
from ActivosFijos.models.hoja_vida_articulo import Hoja_Vida_Articulos
from ActivosFijos.models.orden_servicio import Articulos_OrdenServicio
from ActivosFijos.models.tipos_mantenimiento import Mantenimineto_Tipos
from shared.models.baseModel import BaseModel
from shared.models.periocidades import Periocidades
from shared.models.terceros import Terceros

class CronogramaMantenimiento(BaseModel):
    catArticulo = models.ForeignKey(Categoria_Articulo, on_delete=models.CASCADE)
    fecha_programada = models.DateField() #Fecha de programacion incial 
    tipo_mantenimiento = models.ForeignKey('Mantenimineto_Tipos', on_delete=models.CASCADE, related_name='mantenimiento', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tercero = models.ForeignKey(Terceros, on_delete=models.CASCADE, blank=True, null=True)
    periocidad = models.ForeignKey(Periocidades, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.id
    class meta:
        verbose_name ="Cronograma Mantenimiento"
        verbose_name_plural = 'Cronograma Mantenimiento'
        ordering = ['fecha_programada']

def documetos_bitacora_path(instance, filename):
    IdArticulo = instance.Articulo.Id_Articulo
    IdArticulo = re.sub(r'\W+', '_', str(IdArticulo))
    ext = filename.split('.')[-1]
    return f'img/Articulos/{IdArticulo}/{filename}.{ext}'

class BitacoraMantenimiento(BaseModel):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, blank=True, null=True, related_name='Bitacora')
    fecha_realizacion = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    Novedad = models.TextField(blank=True, null=True)
    orden_servicio = models.ForeignKey(Articulos_OrdenServicio, on_delete=models.CASCADE, blank=True, null=True, related_name='Bitacora')
    tipomantenimiento = models.ForeignKey(Mantenimineto_Tipos, on_delete=models.CASCADE, related_name='Bitacora', blank=True, null=True)
    Estado = models.ForeignKey(Estado_Articulo, on_delete=models.CASCADE, default=1)
    Actualizacion = models.TextField(blank=True, null=True)
    documentos = models.FileField(upload_to=documetos_bitacora_path, blank=True, null=True)

    def __str__(self):
        return f'{self.articulo.Descripcion} - {self.fecha_realizacion}'

    class meta:
        verbose_name ="Bitacora Mantenimiento"
        verbose_name_plural = 'Bitacora Mantenimiento'
        ordering = ['fecha_realizacion']    