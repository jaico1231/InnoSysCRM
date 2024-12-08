import os
import re
from django.db import models
from ActivosFijos.models.articulos import Articulo
from shared.models.baseModel import BaseModel
from shared.models.tipo_anexos import Tipos_Anexos

def cargar_anexo_path(instance, filename):
    IdArticulo = instance.Articulo_FK.Id_Articulo
    IdArticulo = re.sub(r'\W+', '_', str(IdArticulo))
    ext = filename.split('.')[-1]
    return f'img/Articulos/{IdArticulo}/{filename}'

class Anexos_Articulos(BaseModel):
    IdAnexo = models.AutoField ( primary_key=True)
    IdArticulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    TipoAnexo = models.ForeignKey(Tipos_Anexos, on_delete=models.CASCADE, blank=True, null=True)
    # Foto = models.ImageField ('foto del producto', upload_to=('articulos_imagenes/'+ IdArticuloFK.IdArticulo +'/'), blank=True, null=True)
    Archivo = models.FileField('foto del producto', upload_to=cargar_anexo_path, blank=True, null=True)

    def __str__(self):
        return f'Anexos de {self.IdArticuloFK.Descripcion}'
        # return str((self.IdArticuloFK)+" "+(self.IdArticuloFK.Descripcion))

    class meta:
        verbose_name ="Anexos_Articulos"
        verbose_name_plural = 'Anexos_Articulos'
        ordering = ['IdArticuloFK']
