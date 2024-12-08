
from django.db import models
import os
import re

import ActivosFijos
from ActivosFijos.models.areas_trabajo import Areas_Trabajo
from ActivosFijos.models.categoria_articulos import Categoria_Articulo
# ]from ActivosFijos.models 
from ActivosFijos.models.marcas import Marcas
from shared.models.baseModel import BaseModel
from shared.models.terceros import Terceros
from ActivosFijos.models.tipo_articulo import TipoArticulo



def Cargar_imagenes_articulos_path(instance, filename):
    # Obtener el número de documento del tercero
    IdArticulo = instance.Articulo.Id_Articulo
    # Reemplazar espacios en blanco por guiones bajos y eliminar caracteres especiales
    IdArticulo = re.sub(r'\W+', '_', str(IdArticulo))
    # Obtener la extensión del archivo
    ext = filename.split('.')[-1]
    # Devolver la ruta de subida del archivo
    # return os.path.join('archivos_terceros', IdArticulo, f'{instance.IdArticuloFK.IdArticulo}/{filename}')
    return f'img/Articulos/{IdArticulo}/{filename}'
#Creacion de la tabla articulo
class Articulo(BaseModel):
    Id_Articulo = models.AutoField ( primary_key=True)
    Descripcion = models.CharField(max_length=250)
    codigo = models.CharField(max_length=50, blank=True, unique=True, null=True)
    GrupoArticulo_FK = models.ForeignKey(Categoria_Articulo, on_delete=models.CASCADE, blank=True, null=True) #relacion con el
    Marca_FK = models.ForeignKey(Marcas, on_delete=models.CASCADE, blank=True, null=True)
    Modelo = models.CharField (max_length=250, blank=True, null=True)
    Serie =  models.CharField (max_length=250, unique=True, blank=True, null=True)
    Area_FK = models.ForeignKey(Areas_Trabajo, on_delete=models.CASCADE, blank=True, null=True)
    Observaciones = models.TextField(blank=True, null=True)
    Costo = models.DecimalField(max_digits=40, blank=True, decimal_places=3,  null=True)
    Proveedor_FK = models.ForeignKey(Terceros, on_delete=models.CASCADE, blank=True, null=True)
    TipoArticulo_FK = models.ForeignKey(TipoArticulo, on_delete=models.CASCADE, blank=True, null=True)
    Imagen = models.ImageField(upload_to=Cargar_imagenes_articulos_path, blank=True, null=True)
    
    def __str__(self):
        return f'{self.Descripcion}'
    
        
    class meta:
        verbose_name ="Articulo"
        verbose_name_plural = 'Articulo'
        ordering = ['codigo']
    