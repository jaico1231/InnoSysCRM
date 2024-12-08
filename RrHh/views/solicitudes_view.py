from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from RrHh.models.permiso_laboral import Permiso_Laboral
from RrHh.forms.permiso_laboralform import *
from RrHh.models.tipo_formato_carta import Tipo_Formato_Carta


# class Permiso_Laboral(CreateView):
#     template_name = 'solicitudes/solicitud.html'
#     form_class = Permiso_Laboral_EmpleadoForm
#     success_url = reverse_lazy('RrHh:Listar_Solicitudes')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tipo_documento'] = Tipo_Formato_Carta.objects.filter(TipoUsuario_FK=1)
#         #cambiar el nombre del form en el template
#         context['Permiso_Form'] = context['form']
#         context['title'] = 'Solicitudes'
#         context['entity'] = 'Solicitudes'
#         context['list_url'] = reverse_lazy('RrHh:Listar_Solicitudes')
#         return context
    
