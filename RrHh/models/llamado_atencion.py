import re
from django.db import models
from shared.models.user import User
from shared.models.baseModel import BaseModel

from RrHh.models.hoja_vida import Hoja_Vida

class Llamado_Atencion(BaseModel):
    idllamado_atencion = models.AutoField(primary_key=True)
    colaborador = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='Colaborador_Infractor')
    fecha_infraccion = models.DateField()
    Autorizado_por = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='Llamado_Autorizado_por')
    acciones = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.idllamado_atencion} {self.colaborador}'
    
class Descargos(BaseModel):
    iddescargos = models.AutoField(primary_key=True)
    Llamado_Atencion = models.ForeignKey(Llamado_Atencion, on_delete=models.CASCADE, related_name='Descargos_Llamado_Atencion')
    fecha_descargo = models.DateField()
    autorizado_por = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='Descargos_Autorizado_por')
    acciones = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.iddescargos} {self.Llamado_Atencion}'
def upload_to_anexos(instance, filename):
    numero_identificacion = instance.Descargos_FK.Llamado_Atencion.colaborador.numero_identificacion
    numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
    ext = filename.split('.')[-1]
    return f'DOCUMENTOS/{numero_identificacion}/anexos_descargos/{filename}.{ext}'

class Cuestionario_Descargos(BaseModel):
    idcuestionario_descargos = models.AutoField(primary_key=True)
    Descargos_FK = models.ForeignKey(Descargos, on_delete=models.CASCADE, related_name='Cuestionario_del_Descargos', null=True, blank=True)
    preguntas = models.CharField(max_length=300, null=True, blank=True)
    respuestas = models.CharField(max_length=300, null=True, blank=True)
    anexos = models.FileField(upload_to=upload_to_anexos, null=True, blank=True)

    def __str__(self):
        return f'{self.idcuestionario_descargos} {self.Descargos}'