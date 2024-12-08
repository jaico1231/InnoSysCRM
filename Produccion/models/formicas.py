from django.db import models
from shared.models.baseModel import BaseModel

class Grupo_Formica(BaseModel):
    grupo = models.CharField(max_length=100)

    def __str__(self):
        return self.grupo
    
    class Meta:
        verbose_name = 'GrupoFormica'
        verbose_name_plural = 'GruposFormica'
        ordering = ['-id']

class Formica(BaseModel):
    descripcion = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo_Formica, on_delete=models.CASCADE, related_name='formica')
    
    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'Formica'
        verbose_name_plural = 'Formicas'
        ordering = ['-id']

class Medidas(BaseModel):
    medida = models.CharField(max_length=100)
    Descripcion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.medida

    class Meta:
        verbose_name = 'Medida'
        verbose_name_plural = 'Medidas'
        ordering = ['-id']

class Precio_Superficie(BaseModel):
    Formica_FK = models.ForeignKey(Formica, on_delete=models.CASCADE, related_name='Superficie')
    Medida_FK = models.ForeignKey(Medidas, on_delete=models.CASCADE, related_name='Superficie')
    CFT = models.DecimalField("Cliente Final Con Transporte",max_digits=10, decimal_places=2)
    CFEF = models.DecimalField("Cliente Final Entrega en Fabrica",max_digits=10, decimal_places=2)
    PD = models.DecimalField("Distribuidor",max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.Formica_FK} - {self.Medida_FK} - {self.CFT} - {self.CFEF} - {self.PD}"

    class Meta:
        verbose_name = 'PrecioSuperficie'
        verbose_name_plural = 'PreciosSuperficies'
        ordering = ['-id']
