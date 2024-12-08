from django.db import models
from django.utils import timezone
from shared.models.baseModel import BaseModel
from ActivosFijos.models import estado_actividad
from shared.models import estado
from shared.models.user import User


class MateriaPrima(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'MateriaPrima'
        verbose_name_plural = 'MateriaPrimas'
        ordering = ['-id']    

class ProcesoProduccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    materiaprima = models.ManyToManyField(MateriaPrima, through='MateriaPrimaUsada', related_name='procesos')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'ProcesoProduccion'
        verbose_name_plural = 'ProcesosProduccion'
        ordering = ['-id']
    
class MateriaPrimaUsada(models.Model):
    proceso = models.ForeignKey(ProcesoProduccion, on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    cantidad_usada = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.proceso} - {self.materia_prima} - {self.cantidad_usada}"

    class Meta:
        verbose_name = 'MateriaPrimaUsada'
        verbose_name_plural = 'MateriaPrimaUsadas'
        ordering = ['-id']
    
class ProductoTerminado(models.Model):
    nombre = models.CharField(max_length=100)
    proceso_produccion = models.ForeignKey(ProcesoProduccion, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    cantidad_producida = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'ProductoTerminado'
        verbose_name_plural = 'ProductosTerminados'
        ordering = ['-id']

class EvaluacionCalidad(models.Model):
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=100)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Evaluación de {self.producto.nombre} el {self.fecha_evaluacion}"
class EntradaSalida(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    materiaprima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, related_name='movimientos', null=True, blank=True)
    producto_terminado = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE, related_name='movimientos', null=True, blank=True)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    autorizado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='aut_a')
    # genera un campo estado donde diga si fue entregado o recibido
    ESTADO_CHOICES = [
        ('entregado', 'Entregado'),
        ('recibido', 'Recibido'),
    ]
    movimiento = models.CharField(max_length=10, choices=ESTADO_CHOICES, blank=True, null=True) #es el estado del movimiento que se esta realizando
    estado_fk = models.ForeignKey(estado_actividad.Estado_Actividad, on_delete=models.CASCADE, null=True, blank=True, related_name='estado_p')
    observaciones = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Actualiza la cantidad disponible en Materia Prima o Producto Terminado
        if self.tipo == 'entrada':
            if self.materiaprima:
                self.materiaprima.cantidad_disponible += self.cantidad
                self.materiaprima.save()
            elif self.producto_terminado:
                self.producto_terminado.cantidad_disponible += self.cantidad
                self.producto_terminado.save()
        elif self.tipo == 'salida':
            if self.materiaprima:
                if self.materiaprima.cantidad_disponible >= self.cantidad:
                    self.materiaprima.cantidad_disponible -= self.cantidad
                    self.materiaprima.save()
                else:
                    raise ValueError("No hay suficiente materia prima disponible para la salida.")
            elif self.producto_terminado:
                if self.producto_terminado.cantidad_disponible >= self.cantidad:
                    self.producto_terminado.cantidad_disponible -= self.cantidad
                    self.producto_terminado.save()
                else:
                    raise ValueError("No hay suficiente producto terminado disponible para la salida.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.cantidad} unidades de {'materia prima' if self.materiaprima else 'producto terminado'}"

    class Meta:
        verbose_name = 'EntradaSalida'
        verbose_name_plural = 'EntradasSalidas'
        ordering = ['-id']

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
