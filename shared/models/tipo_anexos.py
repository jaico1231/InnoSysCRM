from django.db import models

from shared.models.baseModel import BaseModel


#DEFINE SI EL ANEXO ES UNA IMAGEN, UNA FACTURA,
# DOCUMENTO DE ENTREGA, REMISION, COMPROBANTE DE PAGO, etc.

class Tipos_Anexos(BaseModel):
    Id_TipoDocumento =  models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250)
    Observacion = models. CharField(max_length=400, blank=True, null=True)
    Activo = models.BooleanField("activo", default= True)#variable activo
    def __str__(self):
        return str(self.Descripcion)
    class meta:
        verbose_name ="TipoDocumento"
        verbose_name_plural = 'TipoDocumento'
        ordering = ['Descripcion']
