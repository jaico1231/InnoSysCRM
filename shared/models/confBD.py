from django.db import models
from shared.models.baseModel import BaseModel


class TipoDB(models.Model):
    tipo = models.CharField(max_length=50)
    titulo = models.CharField(max_length=50)
    def __str__(self):
        return self.tipo    
    class Meta:
        verbose_name="Tipo de Base de Datos"
        verbose_name_plural = 'Tipos de Base de Datos'
        ordering = ['tipo']

class ConexionBD(BaseModel):
    tipo = models.ForeignKey(TipoDB, on_delete=models.CASCADE)
    usuario=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    port=models.IntegerField()
    dominio=models.CharField(max_length=50)
    def __str__(self):
        return str(f'self.usuario')

    class Meta:
        verbose_name="Conexion de Base de Datos"
        verbose_name_plural = 'Conexion de Base de Datos'
        ordering = ['usuario']
        unique_together=('usuario', 'dominio')
