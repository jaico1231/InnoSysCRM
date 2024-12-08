

import datetime
from shared.models.baseModel import *
from RrHh.models.contrato_laboral import *
from RrHh.models.hoja_vida import *
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Asistencia(BaseModel):
    empleado = models.TextField()
    id_biometrico = models.IntegerField()
    entrada = models.DateTimeField()
    salida = models.DateTimeField()

    def __str__(self):
        return self.empleado
    def clean(self):
        # Valida que entrada y salida sean del tipo datetime
        if not isinstance(self.entrada, datetime.datetime):
            raise ValidationError(_('La entrada debe ser un objeto datetime.'))
        if not isinstance(self.salida, datetime.datetime):
            raise ValidationError(_('La salida debe ser un objeto datetime.'))

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'


# Horas extras 
class ConfiguracionNomina(BaseModel):
    nombre = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Concepto(BaseModel):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, choices=[('Ingreso', 'Ingreso'), ('Descuento', 'Descuento')])

    def __str__(self):
        return self.nombre
    
class NovedadNomina(BaseModel):
    contrato = models.ForeignKey(Contrato_Laboral, on_delete=models.CASCADE, related_name='novedades_nomina')
    # control de asistencia
    asistencias = models.ForeignKey(Asistencia, on_delete=models.CASCADE, null=True, blank=True)
    horas_extra_normal = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    horas_extra_nocturna = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    horas_extra_dominical_diurna = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    horas_extra_dominical_nocturna = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    horas_extra_festivo_diurno = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    horas_extra_festivo_nocturno = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # Permisos y llegadas tarde
    horas_permiso_laboral = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    horas_llegada_tarde = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # Otros conceptos
    vacaciones = models.BooleanField(default=False)
    suspensiones = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'NovedadNomina'
        verbose_name_plural = 'NovedadesNomina'

    def __str__(self):
        return self.contrato