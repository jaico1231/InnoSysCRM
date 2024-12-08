from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_notifications(request):
    # Asegúrate de que tu modelo de notificaciones está importado
    from shared.models.notificaciones import Notification

    # Obtén las notificaciones para el usuario actual
    notifications = Notification.objects.filter(user=request.user)

    # Convierte las notificaciones en una lista de diccionarios
    notifications_list = notifications.values('id', 'message', 'timestamp')

    # Convierte los objetos datetime a strings para que puedan ser serializados a JSON
    for notification in notifications_list:
        notification['timestamp'] = notification['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    # Devuelve las notificaciones como un objeto JSON
    return JsonResponse({'notifications': list(notifications_list)})
