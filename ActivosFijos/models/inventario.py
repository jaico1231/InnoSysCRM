from django.db import models
from shared.models.baseModel import BaseModel
from shared.models.user import User
from .articulos import Articulo
from .tipo_registroinventario import TipoRegistroInventario



class Inventario(BaseModel):
    IdInventario = models.AutoField ( primary_key=True)
    IdArticulo_FK = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    Cantidad = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tipo_registro = models.ForeignKey(TipoRegistroInventario, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Inventario de {self.IdArticulo_FK.Descripcion}'
        # return str((self.IdArticuloFK)+" "+(self.IdArticuloFK.Descripcion))

    class meta:
        verbose_name ="Inventario"
        verbose_name_plural = 'Inventario'
        ordering = ['IdArticuloFK']
