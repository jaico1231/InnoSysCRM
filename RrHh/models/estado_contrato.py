from django.db import models

    # "Activo",
    # "Terminado",
    # "Suspendido",
class estado_contrato(models.Model):
    estado = models.CharField(max_length=10)
    def __str__(self):
        return self.estado
    class Meta:
        verbose_name="estado_contrato"
        verbose_name_plural = 'estado_contrato'
        ordering = ['estado']
        