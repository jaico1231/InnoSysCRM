from django.db import models
from shared.models.baseModel import BaseModel
from shared.models.estado import Estado

#Creacion de tabla grupo de articulos(categoria:cristaleria, sistemas, electrodomesticos)
class Categoria_Articulo(BaseModel):
    Id_GrupoArticulo =   models.AutoField(primary_key=True )
    Descripcion = models.CharField(max_length=250, unique=True)
    Observacion = models. CharField(max_length=400, blank=True, null=True)
    Estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default=1)#Modulo Administracion
    FechaCreacion = models.DateTimeField('fecha creación', auto_now_add=True )
    
    def __str__(self):
        return str(self.Descripcion)
    class meta:
        verbose_name ="GrupoArticulos"
        verbose_name_plural = 'GrupoArticulos'
        ordering = ['Descripcion']
