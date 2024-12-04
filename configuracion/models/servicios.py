from django.db import models
from shared.models.terceros import Terceros
from shared.models.baseModel import BaseModel


from django.db import models
from shared.models.baseModel import BaseModel

class Servicios(BaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    estado = models.BooleanField(default=True)
    codigo = models.CharField(max_length=100, unique=True, null=True, blank=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = 'Servicios'
        ordering = ['nombre']

class Paquetes(BaseModel):
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    codigo = models.CharField(max_length=100, unique=True, null=True, blank=True)
    precio = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    servicios = models.ManyToManyField(Servicios, through='PaquetesServicios', related_name='paquetes')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = 'Paquetes'
        ordering = ['nombre']

class PaquetesServicios(BaseModel):
    paquete = models.ForeignKey(Paquetes, on_delete=models.CASCADE, related_name='paquetes_servicios')
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, related_name='servicios_paquetes')
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.paquete} - {self.servicio}'

    class Meta:
        verbose_name = "Paquete-Servicio"
        verbose_name_plural = 'Paquetes-Servicios'
        ordering = ['paquete']
        unique_together = ('paquete', 'servicio')


class Medicos(BaseModel):
    tercero = models.ForeignKey(Terceros, on_delete=models.CASCADE, related_name='terceros')
    comision = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    descuento = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)    

    def __str__(self):
        return f'{self.tercero.Nombre} {self.tercero.Apellido}'

    class Meta:
        verbose_name = "Medico"
        verbose_name_plural = 'Medicos'
        ordering = ['tercero']

class Medico_paquetes(BaseModel):
    medico = models.ForeignKey(Medicos, on_delete=models.CASCADE, related_name='medicos_paquetes')
    paquete = models.ForeignKey(Paquetes, on_delete=models.CASCADE, related_name='paquetes_medicos')

    def __str__(self):
        return f'{self.medico} - {self.paquete}'

    class Meta:
        unique_together = ('medico', 'paquete')
        verbose_name = "Medico-Paquete"
        verbose_name_plural = 'Medicos-Paquetes'
        ordering = ['medico']