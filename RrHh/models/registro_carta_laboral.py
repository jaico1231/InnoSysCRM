
from django.db import models

from shared.models.baseModel import BaseModel
from RrHh.models.contrato_laboral import Contrato_Laboral
from RrHh.models.tipo_formato_carta import Tipo_Formato_Carta

# si son cartas laborales por que tengo tipos de cartas 

class Registro_Carta_Laboral(BaseModel):
    contrato_laboral = models.ForeignKey(Contrato_Laboral, on_delete=models.CASCADE, related_name='registros_carta_laboral')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tipo_cartaFK = models.ForeignKey(Tipo_Formato_Carta, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Registro Carta Laboral"
        verbose_name_plural = "Registros Cartas Laborales"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Carta Laboral para {self.contrato_laboral.hoja_vida_FK.nombre} {self.contrato_laboral.hoja_vida_FK.apellido}"
