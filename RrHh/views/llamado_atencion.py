from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from RrHh.forms.llamado_atencion_form import Llamado_AtencionForm
from RrHh.models.llamado_atencion import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class Listar_Llamado_Atencion(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'RrHh.view_llamado_atencion'
    model = Llamado_Atencion
    template_name = 'llamado_atencion/Listar_Llamado_Atencion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Llamado de Atención'
        context['entity'] = 'Llamado de Atención'
        return context

class Crear_Llamado_Atencion(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'RrHh.add_llamado_atencion'
    form_class = Llamado_AtencionForm
    template_name = 'llamado_atencion/crear_llamado_Atencion.html'
    success_url = reverse_lazy('RrHh:Listar_HV')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.creado_por = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Llamado de Atención'
        context['entity'] = 'Llamado de Atención'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
    
class Editar_Llamado_Atencion(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'RrHh.change_llamado_atencion'
    model = Llamado_Atencion
    form_class = Llamado_AtencionForm
    template_name = 'llamado_atencion/Editar_Llamado_Atencion.html'
    success_url = reverse_lazy('RrHh:Listar_HV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Llamado de Atención'
        context['entity'] = 'Llamado de Atención'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_HV')
        return context


class Eliminar_Llamado_Atencion(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'RrHh.change_llamado_atencion'
    model = Llamado_Atencion
    form_class = Llamado_AtencionForm
    template_name = 'llamado_atencion/Eliminar_Llamado_Atencion.html'
    success_url = reverse_lazy('RrHh:Listar_HV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Llamado de Atención'
        context['entity'] = 'Llamado de Atención'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_HV')
        return context

class Historial_Llamado_Atencion(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'RrHh.view_llamado_atencion'
    template_name = 'llamado_atencion/historial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hv = self.kwargs['pk']  # id de la hoja de vida        
        llamados_atencion = Llamado_Atencion.objects.filter(colaborador=hv).prefetch_related('Descargos_Llamado_Atencion__Cuestionario_del_Descargos')
        
        context['llamados_atencion'] = [
            {
                'llamado': llamado,
                'descargos': llamado.Descargos_Llamado_Atencion.all()
            }
            for llamado in llamados_atencion
        ]
        context['cantidad_llamados'] = llamados_atencion.count()
        context['id_hv'] = hv        
        context['title'] = 'Historial Llamado de Atención'
        context['entity'] = 'Llamado de Atención'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_HV')
        return context

    
# class Historial_Llamado_Atencion(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
#     permission_required = 'RrHh.view_llamado_atencion'
#     template_name = 'llamado_atencion/historial.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         hv= self.kwargs['pk']        
#         hojas_de_vida = Hoja_Vida.objects.all().filter(pk=self.kwargs['pk']).first()
#         Llamados_Atencion = Llamado_Atencion.objects.all().filter(colaborador=hv)
#         descargos = None
#         listado = None
#         if Llamados_Atencion.exists():
#             context['cantidad_LL_AT'] = Llamados_Atencion.count()
#             descargos = Descargos.objects.filter(Llamado_Atencion=Llamados_Atencion.first())
#             print(descargos)
#             if descargos.exists():
#                 pass
#                 listado = Cuestionario_Descargos.objects.all().filter(Descargos_FK=descargos.first())
#                 print(listado)
#             else:
#                 descargos = None
#         else:
#             Llamados_Atencion = None
#         context['listado'] = listado
#         context['Descargos'] = descargos
#         context['hojas_de_vida'] = hojas_de_vida
#         context['Llamados_Atencion'] = Llamados_Atencion
        
#         context['title'] = 'Historial Llamado de Atención'
#         context['entity'] = 'Llamado de Atención'
#         context['list_url'] = reverse_lazy('RrHh:Listar_HV')
#         context['cancel_url'] = reverse_lazy('RrHh:Listar_HV')
#         return context