from django.db import models
from shared.models.baseModel import BaseModel
from RrHh.models.hoja_vida import *
from RrHh.models.contrato_laboral import *
class DatosFinancierosEmpleado(BaseModel):
    contrato = models.ForeignKey(Contrato_Laboral, on_delete=models.CASCADE, related_name='datos_financieros')
    banco = models.CharField(max_length=255)
    numero_cuenta = models.CharField(max_length=50)
    tipo_cuenta = models.CharField(max_length=50)

    def __str__(self):
        return self.contrato

    class Meta:
        verbose_name = 'DatosFinancieros'
        verbose_name_plural = 'DatosFinancieros'
        ordering = ['-id']

class AuxilioNoPrestacional(BaseModel):
    colaborador = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='Aux_No_Prest')
    descripcion = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.colaborador

    class Meta:
        verbose_name = 'AuxilioNoPrestacional'
        verbose_name_plural = 'AuxilioNoPrestacional'
        ordering = ['-id']

#Rodamientos no prestacionales
class RodamNoPresta(BaseModel):
    colaborador = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='Rod_No_Prest')
    descripcion = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'RodamNoPresta'
        verbose_name_plural = 'RodamNoPresta'
        ordering = ['-id']

class DescuentoAdicional(BaseModel):
    colaborador = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='Desc_Adicional')
    descripcion = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.colaborador

    class Meta:
        verbose_name = 'DescuentoAdicional'
        verbose_name_plural = 'DescuentoAdicional'
        ordering = ['-id']
    
class CampoAdicionalLiquidacion(models.Model):
    colaborador = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='Adicional_Liquidacion')
    descripcion = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.colaborador

    class Meta:
        verbose_name = 'CampoAdicionalLiquidacion'
        verbose_name_plural = 'CampoAdicionalLiquidacion'
        ordering = ['-id']
    
class Tabla_Precios_Rutas(BaseModel):
    nombre = models.CharField(max_length=255)
    kmh = models.CharField('Kilometros Recorrido', max_length=255)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.kmh} "
    
    class Meta:
        verbose_name = 'TablaPreciosRutas'
        verbose_name_plural = 'TablaPreciosRutas'
        ordering = ['-id']

class RutaVisitas(BaseModel):
    colaborador = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='rutas_visita')
    ruta = models.CharField(max_length=255)
    valor = models.ForeignKey(Tabla_Precios_Rutas, on_delete=models.CASCADE, related_name='rutas_visita')

    def __str__(self):
        return f"{self.colaborador}"

    class Meta:
        verbose_name = 'RutaVisita'
        verbose_name_plural = 'RutaVisita'
        ordering = ['-id']