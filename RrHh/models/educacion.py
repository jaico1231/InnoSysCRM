
from django.db import models

from shared.models.baseModel import BaseModel
from shared.models.geografia import Paises
from RrHh.models.hoja_vida import Hoja_Vida, upload_to_hv
# from .paises import Paises
# from .hoja_vida import Hoja_Vida
# from .upload_to import upload_to_hv
class Educacion(BaseModel):
    IdEducacion = models.AutoField(primary_key=True)
    hoja_vida_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='educacion', null=True, blank=True)
    institucion_EDU = models.CharField(max_length=100, null=True, blank=True)
    titulo_EDU = models.CharField(max_length=100, null=True, blank=True)
    pais_EDU = models.ForeignKey(Paises, on_delete=models.CASCADE, related_name='educacion', null=True, blank=True)
    duracion_EDU = models.IntegerField(null=True, blank=True)
    TextoUnidad_EDU = models.CharField(max_length=100, null=True, blank=True)
    fecha_inicio_EDU = models.DateField(null=True, blank=True)
    fecha_fin_EDU = models.DateField(null=True, blank=True)
    upload_docs_EDU = models.FileField(upload_to=upload_to_hv, null=True, blank=True)
    def __str__(self):
        return f"{self.hoja_vida_FK} {self.titulo_EDU}"
    class Meta:
        verbose_name="Educacion"
        verbose_name_plural = 'Educacion'
        ordering = ['-IdEducacion']
