
from django.db import models
#Para que son los tipos de permisos

class Tipo_Permiso(models.Model):
    IdTipoPermiso = models.AutoField(primary_key=True)
    TipoPermiso = models.CharField(max_length=100)
    def __str__(self):
        return self.TipoPermiso
    class Meta:
        verbose_name="TipoPermiso"
        verbose_name_plural = 'TipoPermiso'
        ordering = ['TipoPermiso']