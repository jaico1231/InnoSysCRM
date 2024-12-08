from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.core import serializers
from RrHh.forms.creacion_documentos_form import Creacion_DocumentosForm
from RrHh.models.hoja_vida import Hoja_Vida
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin


class Generar_Carta(LoginRequiredMixin, CreateView):
    template_name = 'HV/formatos/Select_formato.html'
    form_class = Creacion_DocumentosForm
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        json_serializers = serializers.get_serializer("json")()

        id=self.kwargs.get('pk')
        context['id'] = id
        
        Hoja_vida = Hoja_Vida.objects.filter(IdHojaVida=id)
        time=datetime.datetime.now()

        context['HV'] = Hoja_vida
        context['HV_json'] = json_serializers.serialize( Hoja_vida, ensure_ascii=False)
        context['title'] = 'Generar Carta'
        context['entity'] = 'Generar Carta'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context