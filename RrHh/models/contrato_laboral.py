
from django.db import models
import re
from shared.models.baseModel import BaseModel
from shared.models.datos_empresa import DatosIniciales
from shared.models.terceros import Terceros
from RrHh.models.estado_contrato import estado_contrato
from RrHh.models.tipo_contrato import tipo_contrato
from RrHh.models.cargo import Cargo
from RrHh.models.hoja_vida import Hoja_Vida
from MacroProcesos.models.macroprocesos import Cargo_Macroprocesos

def upload_contrato(instance, filename):
    numero_identificacion = instance.hoja_vida_FK.numero_identificacion
    numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
    ext = filename.split('.')[-1]
    return f'DOCUMENTOS/{numero_identificacion}/CONTRATO/{filename}{ext}'
def upload_renuncia(instance, filename):
    numero_identificacion = instance.Contrato_Laboral_FK.hoja_vida_FK.numero_identificacion
    numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
    ext = filename.split('.')[-1]
    return f'DOCUMENTOS/{numero_identificacion}/RENUNCIA/{filename}.{ext}'

# Modelo para los contratos laborales
class Contrato_Laboral(BaseModel):
    hoja_vida_FK = models.ForeignKey(Hoja_Vida, on_delete=models.CASCADE, related_name='contratos_laboral')
    empresa = models.ForeignKey(DatosIniciales,default=1, on_delete=models.CASCADE)#cargar datos empleador
    cargo_macro = models.ForeignKey(Cargo_Macroprocesos, on_delete=models.CASCADE, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField('fecha de inicio contrato')
    fecha_inicio_laboral = models.DateField('Fecha de Inicio Labores')
    fecha_fin = models.DateField('Fecha Fin Contrato',null=True, blank=True)
    tiempo_contrato = models.CharField('Meses de contrato',max_length=100,null=True, blank=True)
    tipo_contratoFK = models.ForeignKey(tipo_contrato, on_delete=models.CASCADE)
    CentFormacion = models.CharField('Centro de formacion',max_length=20,null=True, blank=True)
    Prog_Formacion = models.CharField('Programa de formacion',max_length=20,null=True, blank=True)
    grupo_formacion = models.CharField('Grupo de formacion',max_length=20,null=True, blank=True)
    salario = models.DecimalField(max_digits=40, decimal_places=2)    
    fecha_renuncia = models.DateField('Fecha de Renuncia', null=True, blank=True )  # renuncia efectiva
    fecha_notificacion_renuncia = models.DateField('Fecha de Notificacion Renuncia', null=True, blank=True)
    carta_renuncia = models.FileField('Carta de Renuncia', upload_to=upload_renuncia, null=True, blank=True)
    fecha_despido = models.DateField('Fecha de Despido', null=True, blank=True)
    motivo_fin_contrato = models.TextField('Motivo Fin de Contrato', null=True, blank=True)
    empresa_formacion = models.ForeignKey(Terceros, on_delete=models.CASCADE, null=True, blank=True)
    estado_FK = models.ForeignKey(estado_contrato, on_delete=models.CASCADE,related_name='estado_contrato', null=True, blank=True)
    
    class Meta:
        verbose_name="ContratoLaboral"
        verbose_name_plural = 'ContratoLaboral'
        ordering = ['-id']

    def __str__(self):
        return f"Contrato ID: {self.id}"


class soportes_contrato(BaseModel):
    idsoportes = models.AutoField(primary_key=True)
    Contrato_Laboral_FK = models.ForeignKey(Contrato_Laboral, on_delete=models.CASCADE)
    nombre_soporte = models.CharField(max_length=100)
    soporte = models.FileField(upload_to=upload_renuncia, null=True, blank=True)


    class Meta:
        verbose_name="SoporteContrato"
        verbose_name_plural = 'SoporteContrato'
        ordering = ['-idsoportes']

    def __str__(self):
        return self.idsoportes


class Actualizar_Contrato(BaseModel):
    Contrato_Laboral_FK = models.ForeignKey(Contrato_Laboral, on_delete=models.CASCADE)
    estado_FK = models.ForeignKey(estado_contrato, on_delete=models.CASCADE,null=True, blank=True)
    fecha_actualizacion = models.DateField('Fecha de Actualizacion')
    salario_anterior = models.TextField(null=True, blank=True)
    salario_nuevo = models.TextField(null=True, blank=True)
    fecha_anterior = models.DateTimeField(auto_now_add=True)
    fecha_nueva = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name="ActualizacionContrato"
        verbose_name_plural = 'ActualizacionContrato'
        ordering = ['-id']

    def __str__(self):
        return self.Contrato_Laboral_FK