from django.db import models
# (1, 'Pre Aprobado'),
# (2, 'Aprobado'),
# (3, 'Re agendado'),
# (4, 'Cancelado'),
# (5, 'En proceso'),
# (6, 'Finalizado'),
class estado_solicitud(models.Model):
    IdEstadoSolicitud = models.CharField(max_length=100)
    estado = models.CharField(max_length=13)
    def __str__(self):
        return self.estado
    class Meta:
        verbose_name="estado_solicitud"
        verbose_name_plural = 'estado_solicitud'
        ordering = ['estado']
