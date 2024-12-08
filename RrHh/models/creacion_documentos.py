from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models.hoja_vida import Hoja_Vida
from RrHh.models.tipo_formato_carta import Tipo_Formato_Carta
from RrHh.models.estado_solicitud import estado_solicitud

class Creacion_Documentos(BaseModel):
    IdDocumentos = models.AutoField(primary_key=True)
    colaborador_FK = models.ForeignKey(User, on_delete=models.CASCADE)
    Tipo_Formato_CartaFK = models.ForeignKey(Tipo_Formato_Carta, on_delete=models.CASCADE)
    propietario_doc = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='propietario', null=True, blank=True)
    fecha_inicio_vacacion = models.DateField(null=True, blank=True)
    fecha_fin_vacacion = models.DateField(null=True, blank=True)
    dias_vacaciones = models.IntegerField(null=True, blank=True)
    fecha_inicio_alternativa = models.DateField(null=True, blank=True)
    fecha_fin_alternativa = models.DateField(null=True, blank=True)
    dias_alternativo = models.IntegerField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    accion_irregular = models.TextField(blank=True, null=True)
    reportes_anexos = models.TextField(blank=True, null=True)
    estado = models.ForeignKey(estado_solicitud, on_delete=models.CASCADE, null=True, blank=True, related_name='estado_creacion_documento')
    
    class Meta:
        verbose_name = "Documentos"
        verbose_name_plural = "Documentos"
        ordering = ['-IdDocumentos']

    def __str__(self):
        return self.IdDocumentos