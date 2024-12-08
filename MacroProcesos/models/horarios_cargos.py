from MacroProcesos.models.macroprocesos import *

class Dias_Laborales_cargos (BaseModel):
    IdHorarioCargo = models.AutoField(primary_key=True)
    Cargo = models.ForeignKey(Cargo_Macroprocesos, on_delete=models.CASCADE, related_name='horarios_cargos', null=True, blank=True)
    Dias_Laborales = models.CharField(max_length=100, null=True, blank=True)
    Observacion = models.CharField(max_length=1000, blank=True, null=True)
    def __str__(self):
        return f"{self.IdHorarioCargo}"

    class Meta:
        verbose_name="HorarioCargo"
        verbose_name_plural = 'HorariosCargos'
        ordering = ['-IdHorarioCargo']

class Horario_cargos (BaseModel):
    IdHorario = models.AutoField(primary_key=True)
    Horario = models.CharField(max_length=100, null=True, blank=True)
    Observacion = models.CharField(max_length=1000, blank=True)
    Descanso_Diurno = models.TimeField(null=True, blank=True)
    Almuerzo = models.TimeField(null=True, blank=True)
    Descanso_Nocturno = models.TimeField(null=True, blank=True)
    es_estandar = models.BooleanField(default=True)  # Define si es un horario estándar o temporal
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.Horario}"

    class Meta:
        verbose_name="Horario"
        verbose_name_plural = 'Horarios'
        ordering = ['-IdHorario']