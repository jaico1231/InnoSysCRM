# import schedule
# import time
# from datetime import timedelta, date
# from django.utils import timezone
# from RrHh.models.contrato_laboral import Contrato_Laboral, Actualizar_Contrato, estado_contrato

# def auto_update_contratos():
#     for contrato in Contrato_Laboral.objects.all():
#         # Obtener la fecha actual
#         fecha_actual = timezone.now().date()
#         # Obtener la fecha de un mes a partir de la fecha actual
#         fecha_limite = fecha_actual + timedelta(days=30)
#         # Filtrar los contratos cuyo fecha_fin es menor a un mes y el estado es activo
#         contratos = Contrato_Laboral.objects.filter(estado_FK=1).filter(fecha_fin__lte=fecha_limite)
        
#         for contrato in contratos:
#             # Crear una instancia de Actualizar_Contrato y guardarla
#             fecha_fin = contrato.fecha_fin
#             fecha_nueva = fecha_fin + timedelta(days=90)
#             # Guardar los datos generados en Actualizar_Contrato
#             Actualizar_Contrato.objects.create(
#                 Contrato_Laboral_FK=contrato,
#                 fecha_actualizacion=fecha_actual,
#                 fecha_anterior=fecha_fin,
#                 fecha_nueva=fecha_nueva,
#                 )
#             updated_at=timezone.now()
#             contrato.fecha_fin = fecha_nueva
#             contrato.save()
#     return f'{contratos.count()} contratos actualizados con éxito.'

# # Programar la ejecución de la función una vez al día
# schedule.every().day.at("00:00").do(auto_update_contratos)

# # Ejecutar el programa de forma continua para que la tarea se ejecute
# while True:
#     schedule.run_pending()
#     time.sleep(1)
#funciona ahora estoy tratando de que se ejecute 1 vez por dia 

from datetime import timedelta, date
from django.utils import timezone
from RrHh.models.contrato_laboral import Contrato_Laboral, Actualizar_Contrato, estado_contrato

def auto_update_contratos():
    for contrato in Contrato_Laboral.objects.all():
        # Obtener la fecha actual
        fecha_actual = timezone.now().date()
        # Obtener la fecha de un mes a partir de la fecha actual
        fecha_limite = fecha_actual + timedelta(days=30)
        # Filtrar los contratos cuyo fecha_fin es menor a un mes y el estado es activo
        contratos = Contrato_Laboral.objects.filter(estado_FK=1).filter(fecha_fin__lte=fecha_limite)
        
        for contrato in contratos:
            # Crear una instancia de Actualizar_Contrato y guardarla
            fecha_fin = contrato.fecha_fin
            fecha_nueva = fecha_fin + timedelta(days=90)
            # Guardar los datos generados en Actualizar_Contrato
            Actualizar_Contrato.objects.create(
                Contrato_Laboral_FK=contrato,
                fecha_actualizacion=fecha_actual,
                fecha_anterior=fecha_fin,
                fecha_nueva=fecha_nueva,
                )
            updated_at=timezone.now()
            contrato.fecha_fin = fecha_nueva
            contrato.save()
    return f'{contratos.count()} contratos actualizados con éxito.'