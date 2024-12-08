
from typing import Iterable
from crum import get_current_user
from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models import estado_solicitud
from RrHh.models.hoja_vida import Hoja_Vida
from RrHh.models.tipo_permiso import Tipo_Permiso
class Permiso_Laboral(BaseModel):
    IdPermiso = models.AutoField(primary_key=True)
    solicitante_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='Solicitante_del_permiso')
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_solicitada = models.DateField()
    tipo_permisoFK = models.ForeignKey(Tipo_Permiso, on_delete=models.CASCADE)
    tiempo_solicitado_horas = models.IntegerField()
    fundamentacion = models.TextField(blank=True, null=True)
    estado_FK = models.ForeignKey(estado_solicitud, on_delete=models.CASCADE, default=5)
    validador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validador', blank=True, null=True)
    fecha_validacion = models.DateField(blank=True, null=True)
    otro_permiso = models.CharField(max_length=100, blank=True, null=True)#que es eso
    observaciones = models.TextField(blank=True, null=True)
    autorizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autorizador', blank=True, null=True)
    fecha_autorizacion = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Permiso Laboral"
        verbose_name_plural = "Permisos Laborales"
        ordering = ['-IdPermiso']

    def __str__(self):
        return self.IdPermiso
