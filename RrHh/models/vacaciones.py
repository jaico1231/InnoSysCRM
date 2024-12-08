import re
from django.db import models
from shared.models.baseModel import BaseModel
from shared.models.user import User
from RrHh.models.estado_solicitud import estado_solicitud
from RrHh.models.hoja_vida import Hoja_Vida

def upload_pdf(instance, filename):
    # Obtener el número de documento del tercero
    numero_identificacion = instance.colaborador_FK.numero_identificacion
    # Reemplazar espacios en blanco por guiones bajos y eliminar caracteres especiales
    numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
    # Obtener la extensión del archivo
    ext = filename.split('.')[-1]
    # Devolver la ruta de subida del archivo
    # return os.path.join('archivos_terceros', IdArticulo, f'{instance.IdArticuloFK.IdArticulo}/{filename}')
    return f'DOCUMENTOS/{numero_identificacion}/VACACIONES/{filename}'

class Vacaciones(BaseModel):
    IdSolicitud = models.AutoField(primary_key=True)
    colaborador_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, null=True, blank=True, related_name='solicitud_vacaciones')
    fecha_inicial = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    dias = models.IntegerField(null=True, blank=True)
    jefe_inmediato = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='jefe_inmediato')#se toma como prevalidacion del supervisor o jefe inmediato mas el estado
    fecha_inicio_alternativa = models.DateField(null=True, blank=True)
    fecha_fin_alternativa = models.DateField(null=True, blank=True)
    dias_alternativo = models.IntegerField(null=True, blank=True)
    fecha_inicio_laboral = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.ForeignKey(estado_solicitud, default=5, on_delete=models.CASCADE, null=True, blank=True, related_name='estado_solicitud_vacaciones')
    file = models.FileField(upload_to=upload_pdf, null=True, blank=True)

    class Meta:
        verbose_name = "Solicitud de vacaciones"
        verbose_name_plural = "Solicitudes de vacaciones"
        ordering = ['-IdSolicitud']

    def __str__(self):
        return str(self.IdSolicitud)
