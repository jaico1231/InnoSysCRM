from MacroProcesos.models.macroprocesos import TipoPersonal
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# @receiver(post_migrate, sender='MacroProcesos')
# def datos_iniciales_macroprocesos(sender, **kwargs):
def datos_iniciales_macroprocesos():
    try:
        TIPO_PERSONAL = [
            ('ADMINISTRATIVO'),
            ('OPERATIVO'),
            ('ADMINISTRATIVO-OPERATIVO'),
            ('TECNICO'),
            ('MANTENIMIENTO'),
            ('SEGURIDAD'),
            ('SERVICIOS'),
            ('OTROS'),
            
        ]
        for tipo in TIPO_PERSONAL:
            TipoPersonal.objects.get_or_create(TipoPersonal = tipo)
        print('Datos iniciales de TIPO_PERSONAL cargados correctamente.')
    except Exception as e:
        print('Error al cargar datos iniciales de TIPO_PERSONAL: ', e)
        