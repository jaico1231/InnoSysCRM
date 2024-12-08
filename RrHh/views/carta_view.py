from django.db import models
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.urls import reverse_lazy

from shared.models.datos_empresa import DatosIniciales
from RrHh.forms.cartas_form import Cartas_Form
from RrHh.models.creacion_documentos import Creacion_Documentos
from django.contrib.auth.mixins import LoginRequiredMixin


class Listar_Carta(LoginRequiredMixin, ListView):
    model = Creacion_Documentos
    template_name = 'cartas/listar_carta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cartas'
        context['create_url'] = reverse_lazy('RrHh:Listar_Cartas')
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        context['entity'] = 'Cartas'
        return context

class Crear_Carta(LoginRequiredMixin, CreateView):
    template_name = 'cartas/solicitar_carta.html'
    form_class = Cartas_Form  # Corregido el nombre del atributo a form_class
    model = Creacion_Documentos
    # contrato =
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        iniciales = DatosIniciales.objects.all()
        context['iniciales'] = iniciales
        context['title'] = 'Crear Carta'
        context['entity'] = 'Crear Carta'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context

class Select_Carta(LoginRequiredMixin, FormView):
    template_name = 'cartas/select_carta.html'
    class_form = Cartas_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carta a Generar'
        context['entity'] = 'Carta a Generar'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context

class Carta_View(LoginRequiredMixin, FormView):
    template_name = 'cartas/apertura_nomina.html'
    class_form = Cartas_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carta de Apertura'
        context['entity'] = 'Carta de Apertura'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context

class Carta_Aceptación_Renuncia_Voluntaria(LoginRequiredMixin, TemplateView):
    template_name = 'cartas/Carta_Aceptacion_Renuncia_Voluntaria.html'
    class_form = Cartas_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carta de Apertura'
        context['entity'] = 'Carta de Apertura'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context
    
class Carta_Negacion_Vacaciones(LoginRequiredMixin, TemplateView):
    template_name = 'cartas/Carta_Negacion_Vacaciones.html'
    class_form = Cartas_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carta Negacion Vacaciones'
        context['entity'] = 'Carta Negacion Vacaciones'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context
class Carta_Aceptacion_Vacaciones_Solicitud(LoginRequiredMixin, TemplateView):
    template_name = 'cartas/Carta_Aceptacion_Vacaciones_Solicitud.html'
    class_form = Cartas_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Aceptacion vacaciones Solicitud'
        context['entity'] = 'Carta de Apertura'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context
    
class Carta_Aceptacion_Vacaciones(LoginRequiredMixin, TemplateView):
    template_name = 'cartas/Carta_Aceptacion_Vacaciones.html'
    class_form = Cartas_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Aceptacion vacaciones'
        context['entity'] = 'Carta de Apertura'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context

class Certificado_Laboral(LoginRequiredMixin, TemplateView):
    template_name = 'cartas/Certificado_Laboral.html'
    class_form = Cartas_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Certificado Laboral'
        context['entity'] = 'Certificado Laboral'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context

class Contrato_Aprendizaje(LoginRequiredMixin, TemplateView):
    template_name = 'cartas/Autorizacion_Tratamiendo_Datos.html'
    class_form = Cartas_Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contrato Aprendizaje'
        context['entity'] = 'Contrato Aprendizaje'
        context['list_url'] = reverse_lazy('RrHh:Listar_Cartas')
        return context