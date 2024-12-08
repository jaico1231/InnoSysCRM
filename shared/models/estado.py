from django.db import models
# #tablas Globales
# Estado de los usuarios 
#  ("Activo", "Activo"),
#  ("Inactivo", "Inactivo"),
#  ("Suspendido", "Suspendido"),
class Estado(models.Model):
    Descripcion = models.CharField(max_length=250)
    Observacion = models.CharField(max_length=1000, blank=True)
    def __str__(self):
        return self.Descripcion
    class Meta:
        verbose_name="Estado"
        verbose_name_plural = 'Estado'
        ordering = ['Descripcion']