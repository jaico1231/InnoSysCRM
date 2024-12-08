from django.db import models
from shared.models.terceros import Terceros

class Naturaleza(models.Model): 
    nombre = models.CharField(max_length=10)
    codigo = models.CharField(max_length=1)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Naturaleza'
        verbose_name_plural = 'Naturaleza'
        ordering = ['-id']

class GrupoCuenta(models.Model):
    codigo = models.CharField(max_length=4, unique=True)
    nombre = models.CharField(max_length=100)
    naturaleza = models.ForeignKey(Naturaleza, on_delete=models.CASCADE, related_name='grupos_cuenta')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = 'GrupoCuenta'
        verbose_name_plural = 'GrupoCuenta'
        ordering = ['-id']

class CuentaMayor(models.Model):
    codigo = models.CharField(max_length=6, unique=True)
    nombre = models.CharField(max_length=100)
    grupo_cuenta = models.ForeignKey(GrupoCuenta, on_delete=models.CASCADE, related_name='cuentas_mayor')
    naturaleza = models.ForeignKey(Naturaleza, on_delete=models.CASCADE, related_name='cuentas_mayor')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = 'CuentaMayor'
        verbose_name_plural = 'CuentaMayor'
        ordering = ['-id']

class SubCuenta(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    cuenta_mayor = models.ForeignKey(CuentaMayor, on_delete=models.CASCADE, related_name='sub_cuentas')
    naturaleza = models.ForeignKey(Naturaleza, on_delete=models.CASCADE, related_name='sub_cuentas')
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = 'SubCuenta'
        verbose_name_plural = 'SubCuenta'
        ordering = ['-id']

class CuentaDetalle(models.Model):
    codigo = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    sub_cuenta = models.ForeignKey(SubCuenta, on_delete=models.CASCADE, related_name='cuentas_detalle')
    naturaleza = models.ForeignKey(Naturaleza, on_delete=models.CASCADE, related_name='cuentas_detalle')
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = 'CuentaAuxiliar'
        verbose_name_plural = 'CuentaAuxiliar'
        ordering = ['-id']

class CuentaAuxiliar(models.Model):
    codigo = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    cuentadetalle = models.ForeignKey(CuentaDetalle, on_delete=models.CASCADE, related_name='cuentas_auxiliares')
    naturaleza = models.ForeignKey(Naturaleza, on_delete=models.CASCADE, related_name='cuentas_auxiliares')
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = 'CuentaAuxiliar'
        verbose_name_plural = 'CuentaAuxiliar'
        ordering = ['-id']
