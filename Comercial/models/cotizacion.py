from django.db import models
from shared.models.baseModel import BaseModel
from shared.models.terceros import Terceros
from Produccion.models.Proceso_Produccion import ProductoTerminado

class Cotizacion(BaseModel):
    # pendiente agregar campo asesor a la tabla
    cliente = models.ForeignKey(Terceros, on_delete=models.CASCADE, related_name='cotizaciones')
    aprobada = models.BooleanField(default=False)

    def __str__(self):
        return {self.id} 

    class Meta:
        verbose_name = 'Cotizacion'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-id']

class DetalleCotizacion(BaseModel):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE, related_name='detalles')#producto en el modulo de produccion
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.cotizacion

    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-id']