
from django.db import models
import re
from shared.models.baseModel import BaseModel
from shared.models.user import User
from shared.models.tipo_documento  import Tipo_Documento
from shared.models.genero import Sexo
from shared.models.geografia import *
from RrHh.models.estado_civil import estado_civil
from RrHh.models.fondo_pension import fondo_pension
from RrHh.models.caja_compensacion import Caja_Compensacion
from RrHh.models.eps import EPS
from RrHh.models.grupo_sanguineo import Grupo_Sanguineo
from RrHh.models.tipo_vivienda import Tipo_Vivienda
from RrHh.models.vivienda import Vivienda


def upload_to_hv(instance, filename):
    # Obtener el número de documento del tercero
    numero_identificacion = instance.numero_identificacion
    # Reemplazar espacios en blanco por guiones bajos y eliminar caracteres especiales
    numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
    # Obtener la extensión del archivo
    ext = filename.split('.')[-1]
    # Devolver la ruta de subida del archivo
    # return os.path.join('archivos_terceros', IdArticulo, f'{instance.IdArticuloFK.IdArticulo}/{filename}')
    return f'DOCUMENTOS/{numero_identificacion}/HV/{filename}'


# Create your models here.
class Hoja_Vida(BaseModel):
    IdHojaVida = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100,null=True, blank=True)
    apellido = models.CharField(max_length=100,null=True, blank=True)
    tipo_documentoFK = models.ForeignKey(Tipo_Documento, on_delete=models.CASCADE)
    sexo= models.ForeignKey(Sexo, on_delete=models.CASCADE, null=True, blank=True)
    numero_identificacion = models.CharField(max_length=50,null=True, blank=True, unique=True)
    nacionalidad_FK = models.ForeignKey(Paises, on_delete=models.CASCADE, null=True, blank=True)
    departamento_FK = models.ForeignKey(Departamentos, on_delete=models.CASCADE, null=True, blank=True)
    Municipio_FK = models.ForeignKey(Municipios, on_delete=models.CASCADE, null=True, blank=True, related_name='municipio')
    pais_residencia = models.ForeignKey(Paises, on_delete=models.CASCADE, null=True, blank=True, related_name='pais_residencia')
    dep_residencia = models.ForeignKey(Departamentos, on_delete=models.CASCADE, null=True, blank=True, related_name='departamento_residencia')
    mun_residencia = models.ForeignKey(Municipios, on_delete=models.CASCADE, null=True, blank=True, related_name='municipio_residencia')
    Barrio_FK = models.ForeignKey(Barrio, on_delete=models.CASCADE, null=True, blank=True)
    fecha_expedicion = models.DateField(null=True, blank=True)
    lugar_expedicion = models.ForeignKey(Municipios, on_delete=models.CASCADE, null=True, blank=True, related_name='lugar_expedicion_cedula')
    Libreta_Militar = models.CharField(max_length=100,null=True, blank=True)
    lugar_expedicion_libreta = models.CharField(max_length=100,null=True, blank=True)
    fecha_expedicion_libreta = models.DateField(null=True, blank=True)
    pais_expedicion_libreta = models.ForeignKey(Paises, on_delete=models.CASCADE, null=True, blank=True, related_name='pais_expedicion_libretaFK')
    Distrito_Libreta = models.CharField(max_length=100,null=True, blank=True)
    Clase_libreta = models.CharField(max_length=100,null=True, blank=True)
    Tarjeta_Profesional = models.CharField(max_length=100,null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    telefono = models.CharField(max_length=20,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    profesion = models.CharField(max_length=100,null=True, blank=True)
    hijos = models.IntegerField(null=True, blank=True)
    vivienda_FK = models.ForeignKey(Vivienda, on_delete=models.CASCADE, null=True, blank=True)
    tipo_vivienda_FK = models.ForeignKey(Tipo_Vivienda, on_delete=models.CASCADE, null=True, blank=True)
    contacto_emergencia = models.CharField(max_length=100,null=True, blank=True)
    parentesco = models.CharField(max_length=100,null=True, blank=True)
    telefono_emergencia = models.CharField(max_length=20,null=True, blank=True)
    fondo_pensionFK = models.ForeignKey(fondo_pension, on_delete=models.CASCADE, null=True, blank=True, related_name='fondo_pensionFK')
    fondo_cesantiasFK = models.ForeignKey(fondo_pension, on_delete=models.CASCADE, null=True, blank=True, related_name='fondo_cesantiasFK')
    CajaCompensacionFK = models.ForeignKey(Caja_Compensacion, on_delete=models.CASCADE, null=True, blank=True)
    eps = models.ForeignKey(EPS, on_delete=models.CASCADE, null=True, blank=True)
    talla_camisa = models.CharField(max_length=10,null=True, blank=True)
    talla_pantalon = models.CharField(max_length=10,null=True, blank=True)
    talla_zapatos = models.CharField(max_length=10,null=True, blank=True)
    grupo_sanguineoFK = models.ForeignKey(Grupo_Sanguineo, on_delete=models.CASCADE, null=True, blank=True)
    estado_civilFK = models.ForeignKey(estado_civil, on_delete=models.CASCADE, null=True, blank=True)
    programa_formacion = models.CharField('Programa de formacion',max_length=50,null=True, blank=True)
    codigo_ficha = models.CharField(max_length=5,null=True, blank=True)
    CentroFormacion = models.CharField(max_length=50, default='SIN ASIGNAR')
    habilidades = models.TextField(null=True, blank=True)
    linkedin = models.CharField(max_length=20, null=True, blank=True)
    twitter = models.CharField(max_length=20, null=True, blank=True)
    facebook = models.CharField(max_length=20, null=True, blank=True)
    instagram = models.CharField(max_length=20, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)
    website = models.CharField(max_length=20, null=True, blank=True)
    imagen = models.ImageField(upload_to=upload_to_hv,default='img/profile/user-1.jpg', null=True, blank=True)
    upload_cv = models.FileField(upload_to=upload_to_hv, null=True, blank=True)
    

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name="Hoja_Vida"
        verbose_name_plural = 'Hoja_Vida'
        ordering = ['nombre','apellido','numero_identificacion']