from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta

from RrHh.forms import Contrato_LaboralForm
from RrHh.models.contrato_laboral import Contrato_Laboral
# from RrHh.views.permiso_laboralView import Listar_Solicitudes
# class dashboard_contratos(ListView):
#     model = Contrato_Laboral
#     template_name = 'Contratos/dashboard.html'
#     form_class = Contrato_LaboralForm

#     def get_queryset(self):
#         # Obtener la fecha actual
#         fecha_actual = timezone.now().date()
#         # Calcular la fecha límite (tres meses a partir de la fecha actual)
#         fecha_limite = fecha_actual + timedelta(days=90)
#         # Obtener los contratos que finalizan en tres meses o menos
#         return Contrato_Laboral.objects.filter(
#             fecha_fin__range=(fecha_actual, fecha_limite)
#         ).order_by('fecha_fin')
 
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # llamar a la vista Listar_Solicitudes y filtrar por estado activo
#         context['solicitudes'] = Listar_Solicitudes.get_queryset(self.request).filter(estado_FK__estado=1)
#         print(context['solicitudes'])
#         context['title'] = 'Contratos a Terminar'
#         context['entity'] = 'Contratos'
#         context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
#         return context