from django.db import models

    # ("Administrador"),
    # ("Usuario"),
class Tipo_Usuario(models.Model):    
    IdTipoUsuario = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    def __str__ (self):
        return str(self.Nombre)
    class Meta:
        verbose_name="Tipo_Usuario"
        verbose_name_plural = 'Tipo_Usuario'
        ordering = ['Nombre']