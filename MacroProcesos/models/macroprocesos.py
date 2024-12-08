from django.db import models
from shared.models.baseModel import BaseModel

#Personal administrativo u Operativo
class TipoPersonal (BaseModel):
    IdTipoPersonal = models.AutoField(primary_key=True)
    TipoPersonal = models.CharField(max_length=100, null=True, blank=True)
    Observacion = models.CharField(max_length=1000, blank=True)
    def __str__(self):
        return f"{self.TipoPersonal}"

    class Meta:
        verbose_name="TipoPersonal"
        verbose_name_plural = 'TipoPersonal'
        ordering = ['-IdTipoPersonal']

class MacroProcesos(BaseModel):
    IdMacroProcesos = models.AutoField(primary_key=True)
    MacroProcesos = models.CharField(max_length=100, null=True, blank=True)
    Observacion = models.CharField(max_length=1000, blank=True)
    def __str__(self):
        return f"{self.MacroProcesos}"

    class Meta:
        verbose_name="MacroProcesos"
        verbose_name_plural = 'MacroProcesos'
        ordering = ['-IdMacroProcesos']

class Proceso (BaseModel):
    IdProceso = models.AutoField(primary_key=True)
    MacroProcesos_FK = models.ForeignKey(MacroProcesos, on_delete=models.CASCADE, related_name='proceso', null=True, blank=True)
    Proceso = models.CharField(max_length=100, null=True, blank=True)
    Observacion = models.CharField(max_length=1000, blank=True)
    def __str__(self):
        return f"{self.Proceso}"

    class Meta:
        verbose_name="Proceso"
        verbose_name_plural = 'Procesos'
        ordering = ['-IdProceso']

class Subprocesos (BaseModel):
    IdSubProceso = models.AutoField(primary_key=True)
    proceso_FK = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name='subproceso', null=True, blank=True)
    SubProceso = models.CharField(max_length=100, null=True, blank=True)
    Observacion = models.CharField(max_length=1000, blank=True)
    dueno = models.ManyToManyField('Cargo_Macroprocesos', related_name='dueno_subproceso', blank=True) #models.CharField(max_length=100, null=True, blank=True)
    gestorriesgo = models.ManyToManyField('Cargo_Macroprocesos', related_name='gestor_subproceso', blank=True) #models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.SubProceso}"

    class Meta:
        verbose_name="SubProceso"
        verbose_name_plural = 'SubProcesos'

class Seccion (BaseModel):
    IdSeccion = models.AutoField(primary_key=True)
    Seccion = models.CharField(max_length=100, null=True, blank=True)
    Observacion = models.CharField(max_length=1000, blank=True)
    def __str__(self):
        return f"{self.Seccion}"

    class Meta:
        verbose_name="Seccion"
        verbose_name_plural = 'Secciones'
        ordering = ['-IdSeccion']

class Cargo_Macroprocesos (BaseModel):
    IdCargo = models.AutoField(primary_key=True)
    subproceso = models.ForeignKey(Subprocesos, on_delete=models.CASCADE, related_name='cargo', null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='cargo', null=True, blank=True)
    tipo_personal_FK = models.ForeignKey(TipoPersonal, on_delete=models.CASCADE, related_name='cargo', null=True, blank=True)
    codigo = models.CharField(max_length=100, null=True, blank=True, unique=True)
    Observacion = models.CharField(max_length=1000, blank=True)
    # tipo_personal
    def __str__(self):
        return f"{self.cargo}"

    class Meta:
        verbose_name="Cargo"
        verbose_name_plural = 'Cargos'
        ordering = ['-IdCargo']
