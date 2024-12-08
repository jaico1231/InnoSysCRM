from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO

from shared.models.tipo_usuario import Tipo_Usuario
from .models import *
from django.db.models.signals import post_migrate
from django.dispatch import receiver

print("ingreso al utils de RrHh")
# @receiver(post_migrate, sender='RrHh')
def datos_iniciales_rrhh():
    ESTADOS_SOLICITUD = [
        
        (1, 'Pre Aprobado'),
        (2, 'Aprobado'),
        (3, 'Re agendado'),
        (4, 'Cancelado'),
        (5, 'En proceso'),
        (6, 'Finalizado'),
    ]
    for Estado in ESTADOS_SOLICITUD:
        estado_solicitud.objects.get_or_create(IdEstadoSolicitud=Estado[0],estado=Estado[1])
    print('Datos iniciales de ESTADOS_SOLICITUD cargados correctamente.')
    
    ESTADO_CONTRATOS = [
        (1, 'Activo'),
        (2, 'Suspendido'),
        (3, 'Terminado'),
    ]

    for estado in ESTADO_CONTRATOS:
        estado_contrato.objects.get_or_create(estado=estado[1])[0]

    print('Datos iniciales de ESTADO_CONTRATOS cargados correctamente.')

    TIPO_CONTRATO = [
        (1, 'Contrato por obra o labor'),
        (2, 'Contrato de trabajo a termino fijo'),
        (3, 'Contrato de trabajo a termino indefinido'),
        (4, 'Contrato de aprendizaje'),
        (5, 'Contrato temporal, ocasional o accidental'),
    ]

    for tipo in TIPO_CONTRATO:
        tipo_contrato.objects.get_or_create(tipo=tipo[1])[0]

    print('Datos iniciales de TIPO_CONTRATO cargados correctamente.')

    CARGO= [
        (1, 'Administrador'),
        (2, 'Analista de sistemas'),
        (3, 'Programador'),
        (4, 'Disenador'),
        (5, 'Desarrollador'),
        (6, 'Operario de TI'),
        (7, 'Contador'),
        (8, 'Gerente'),
        (9, 'Jefe de RrHh'),
        (10, 'Jefe de compras'),
        (11, 'Asistente'),
        (12, 'Auxiliar'),
        (13, 'Teólogo'),
        (14, 'Asistente'),
        (15, 'Secretaria'),
        (16, 'Asesor Comercial'),
        (17, 'Asesor de ventas'),
        (18, 'Asesor de marketing'),
    ]

    for x in CARGO:
        Cargo.objects.get_or_create(cargo=x[1])[0]

    print('Datos iniciales de CARGO cargados correctamente.')

    
    
    TIPO_SANGRE = [
        (1, 'O-'),
        (2, 'A-'),
        (3, 'B-'),
        (4, 'AB-'),
        (5, 'O+'),
        (6, 'A+'),
        (7, 'B+'),
        (8, 'AB+'),
    ]
    for tipo in TIPO_SANGRE:
        Grupo_Sanguineo.objects.get_or_create(grupo=tipo[1])[0]

    print('Datos iniciales de TIPO_SANGRE cargados correctamente.')


    ESTADO_CIVIL = [	
        (1, 'Soltero'),
        (2, 'Casado'),
        (3, 'Divorciado'),
        (4, 'Viudo'),
        (5, 'Union Libre'),
    ]
    for estado in ESTADO_CIVIL:
        estado_civil.objects.get_or_create(Estado=estado[1])[0]

    print('Datos iniciales de ESTADO_CIVIL cargados correctamente.')

    FONDO_PENSION   = [
        (1, 'PROTECCION SA'),
        (2, 'PORVENIR SA'),
        (3, 'COLFONDOS'),
        (4, 'COLPENSIONES'),
        (5, 'OLD MUTUAL SA'),
        (6, 'ASOCIACION COLOMBIANA DE AVIADORES CIVILES ACDAC'),
        (7, 'ECOPETROL'),
        (8, 'FONDO DE PRESTACIONES SOCIALES DEL MAGISTERIO'),
    ]
    for fondo in FONDO_PENSION:
        fondo_pension.objects.get_or_create(fondo=fondo[1])

    print('Datos iniciales de FONDO_PENSION cargados correctamente.')

    ENTIDADES_EPS = [
        (1, 'ALIANSALUD ENTIDAD PROMOTORA DE SALUD S.A.'),
        (2, 'ASOCIACIÓN INDÍGENA DEL CAUCA'),
        (3, 'ASOCIACION MUTUAL SER EMPRESA SOLIDARIA DE SALUD EPS'),
        (4, 'CAPITAL SALUD'),
        (5, 'COMFENALCO  VALLE  E.P.S.'),
        (6, 'COMPENSAR   E.P.S.'),
        (7, 'COOPERATIVA DE SALUD Y DESARROLLO INTEGRAL ZONA SUR ORIENTAL DE CARTAGENA'),
        (8, 'E.P.S.  FAMISANAR LTDA. '),
        (9, 'E.P.S.  SANITAS S.A.'),
        (10, 'EPS  CONVIDA'),
        (11, 'EPS SERVICIO OCCIDENTAL DE SALUD S.A.'),
        (12, 'EPS Y MEDICINA PREPAGADA SURAMERICANA S.A'),
        (13, 'FUNDACION SALUD MIA EPS'),
        (14, 'MALLAMAS'),
        (15, 'NUEVA EPS S.A.'),
        (16, 'SALUD TOTAL S.A.  E.P.S.'),
        (17, 'SALUDVIDA S.A. E.P.S'),
        (18, 'SAVIA SALUD EPS'),

    ]
    for eps in ENTIDADES_EPS:
        EPS.objects.get_or_create(EPS=eps[1])

    print('Datos iniciales de ENTIDADES_EPS cargados correctamente.')


    TIPO_FORMATO_CARTA = [
        (1, 'Carta de Presentacion', 1),
        (2, 'Carta de Reunion', 1),
        (3, 'Carta de Entrevista', 1),
        (4, 'Carta Apertura Cta. de nomina', 1),
        (5, 'Carta Autorizacion de Vacaciones (Negacion)', 1),
        (6, 'Carta Autorizacion de Vacaciones x Solicitud', 1),
        (7, 'Carta Autorizacion de Vacaciones', 1),
        (8, 'Carta Llamado de Atencion (Memorandum)', 1),
        (9, 'Carta Notificacion Accion Irregular', 1),
        (10, 'Carta Reconvucion Administrativa', 1),
        (11, 'Carta Terminacion Vigencia Contractual', 1),
        (12, 'Certificado laboral', 2),
        (15, 'Diligencia de Descargos', 1),
        (16, 'Autorizacion de Tratamiento de Datos Personales Sensibles', 1),
        (18, 'Solicitud Permiso Personal', 2),
        (19, 'Novedades Nomina', 1),
        (20, 'Retiro de Cesantias', 2),
        (21, 'Notificacion Salario (Ajuste al Minimo),', 1),
        (22, 'Notificacion Salario (Incremento Salarial),', 1),
        (23, 'Notificacion Salario (No Ajustadol),', 1),
        (24, 'Otro Si al Contrato - Pago NO Salarial', 1),
        (25, 'Proceso Disciplinario', 1),
        (26, 'Carta Aceptacion de Renuncia Voluntaria', 1)
    ]

    for tipo in TIPO_FORMATO_CARTA:
        Tipo_Formato_Carta.objects.get_or_create(id=tipo[0], tipo=tipo[1], TipoUsuario_FK=Tipo_Usuario(tipo[2]))

    print('Datos iniciales de TIPO_FORMATO_CARTA cargados correctamente.')

    CAJA_DE_COMPENSACION = [
        (1, 'COMFANDI'),
        (2, 'CONFENLCO VALLE'),
    ]

    for tipo in CAJA_DE_COMPENSACION:
        Caja_Compensacion.objects.get_or_create(Caja=tipo[1])

    print('Datos iniciales de CAJA_DE_COMPENSACION cargados correctamente.')

    TIPO_PERMISOS = [
        (1, 'Personal'),
        (2, 'Cita Medica'),
        (3, 'Dia Laboral'),
        (4, 'Licencia'),
        (5, 'Otro'),
    ]

    for tipo in TIPO_PERMISOS:
        Tipo_Permiso.objects.get_or_create(IdTipoPermiso=tipo[0], TipoPermiso=tipo[1])
    
    print('Datos iniciales de TIPO_PERMISOS cargados correctamente.')

    TIPO_NOVEDADES = [
        
        (1, 'Suspencion'),
        (2, 'Incapacidad'),
        (3, 'Vacaciones'),        
        (4, 'Licencia por Calamidad'),
        (5, 'Licencia por Maternidad'),
        (6, 'Licencia por Paternidad'),
        (7, 'Licencia por Luto'),
    ]

    for tipo in TIPO_NOVEDADES:
        Tipo_Novedad.objects.get_or_create(IdTipoNovedad=tipo[0], TipoNovedad=tipo[1])

    print('Datos iniciales de TIPO_NOVEDADES cargados correctamente.')

    TIPO_RETIRO_CESANTIAS = [
        (1, 'Mejoramiento de Vivienda'),
        (2, 'Estudios'),
        (3, 'Compra de Vivienda'),
        (4, 'Finalizacion de Contrato'),
    ]

    for tipo in TIPO_RETIRO_CESANTIAS:
        Tipo_Retiro_Cesantias.objects.get_or_create(IdTipoRetiroCesantias=tipo[0], TipoRetiroCesantias=tipo[1])

    print('Datos iniciales de TIPO_RETIRO_CESANTIAS cargados correctamente.')

    VIVIENDAS = [
        (1, 'Propia'),
        (2, 'Alquilada'),
        (3, 'Familiar'),
        (4, 'Cedida'),
    ]

    for vivienda in VIVIENDAS:
        Vivienda.objects.get_or_create(IdVivienda=vivienda[0], Vivienda=vivienda[1])

    print('Datos iniciales de VIVIENDAS cargados correctamente.')

    TIPO_VIVIENDAS = [
        (1, 'Casa'),
        (2, 'Apartamento'),
        (3, 'Lote'),
    ]

    for tipo in TIPO_VIVIENDAS:
        Tipo_Vivienda.objects.get_or_create(IdTipoVivienda=tipo[0], TipoVivienda=tipo[1])

    print('Datos iniciales de TIPO_VIVIENDAS cargados correctamente.')