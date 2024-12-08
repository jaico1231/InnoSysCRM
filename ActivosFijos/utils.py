from ActivosFijos.models.categoria_articulos import Categoria_Articulo
from ActivosFijos.models.estado_articulo import Estado_Articulo
from ActivosFijos.models.marcas import Marcas
from shared.models.periocidades import Periocidades
from shared.models.tipo_anexos import Tipos_Anexos
from ActivosFijos.models.tipo_registroinventario import TipoRegistroInventario
from ActivosFijos.models.estado_actividad import Estado_Actividad
from ActivosFijos.models.tipo_articulo import TipoArticulo
from ActivosFijos.models.tipos_mantenimiento import Mantenimineto_Tipos
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# @receiver(post_migrate, sender='ActivosFijos')
# def crear_datos_iniciales_ActivosFijos(sender, **kwargs):
def datos_iniciales_ActivosFijos():
    TIPO_REGISTRO_INVENTARIO = [
    ("Entrada", "Entrada"),
    ("Salida", "Salida"),
    ]
    for tipo in TIPO_REGISTRO_INVENTARIO:
        TipoRegistroInventario.objects.get_or_create(Descripcion=tipo[0])
    print('Datos iniciales de TIPO_REGISTRO_INVENTARIO cargados correctamente.')
##########################################################################################
    ESTADOS = [
    ("Realizado", "Realizado"),
    ("En proceso", "En proceso"),
    ("Atrasado", "Atrasado"),
    ("Programado", "Programado"),
    ]
    for estado in ESTADOS:
        Estado_Actividad.objects.get_or_create(Descripcion=estado[0], Observacion=estado[1])
    print('Datos iniciales de ESTADOS cargados correctamente.')
##########################################################################################
    TIPO_ARTICULO = [
    ("Materia prima", "Materia prima"),
    ("Activos fijos", "Activos fijos"),
    ("Proyectos", "Proyectos"),
    ("Otros", "Otros"),
    ]
    for tipo in TIPO_ARTICULO:
        TipoArticulo.objects.get_or_create(Descripcion=tipo[0], Observacion=tipo[1])
    print('Datos iniciales de TIPO_ARTICULO cargados correctamente.')
##########################################################################################
    ESTADOS_ARTICULOS = [
    ("Activo", "Activo"),
    ("En reparacion", "En reparacion"),
    ("En garantia", "En garantia"),
    ("Dado de baja", "Dado de baja"),
    ]
    for estado in ESTADOS_ARTICULOS:
        Estado_Articulo.objects.get_or_create(Descripcion=estado[0], Observacion=estado[1])
    print('Datos iniciales de ESTADOS_ARTICULOS cargados correctamente.')
##########################################################################################
    MARCAS=[
        (1,'HP'),
        (2,'Apple'),
        (3,'Lenovo'),
        (4,'Asus'),
        (5,'Acer'),
        (6,'MSI'),
        (7,'Huawei'),
        (8,'Dell'),
        (9,'Samsung'),
        (10,'Intel'),
        (11,'AMD'),
        ]
    for marca in MARCAS:
        Marcas.objects.get_or_create(Id_marca=marca[0], Descripcion=marca[1])
    print('Datos iniciales de MARCAS cargados correctamente.')
##########################################################################################
    # CATEGORIA_ARTICULO = [
    # ("Cristaleria", "Cristaleria"),
    # ("Sistemas", "Sistemas"),
    # ("Electrodomesticos", "Electrodomesticos"),
    # ("Fileteadoras", "Fileteadoras"),
    # ("Industrial", "Maquinas industriales"),
    # ]
    # for categoria in CATEGORIA_ARTICULO:
    #     Categoria_Articulo.objects.get_or_create(Descripcion=categoria[0], Observacion=categoria[1])
    # print('Datos iniciales de CATEGORIA_ARTICULO cargados correctamente.')
##########################################################################################
    TIPOS_MANTENIMIENTO = [
    ("Preventivo", "Preventivo"),
    ("Correctivo", "Correctivo"),
    ]
    for tipo in TIPOS_MANTENIMIENTO:
        Mantenimineto_Tipos.objects.get_or_create(Descripcion=tipo[0])
    print('Datos iniciales de TIPOS_MANTENIMIENTO cargados correctamente.')

##########################################################################################
    TIPOS_ANEXOS = [
    ("RUT"),
    ("CAMARA Y COMERCIO"),
    ("CERTIFICACION BANCARIA"),
    ("OTROS CERTIFICADOS"),
    ("FACTURA"),
    ]
    for tipo in TIPOS_ANEXOS:
        Tipos_Anexos.objects.get_or_create(Descripcion=tipo[0])
    print('Datos iniciales de TIPOS_ANEXOS cargados correctamente.')

