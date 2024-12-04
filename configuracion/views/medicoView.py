from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import BaseModelForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from shared.models.terceros import Terceros
from configuracion.forms.serviciosForm import MedicosForm
from configuracion.models.servicios import Medico_paquetes, Medicos
from shared.loggin import log_event
from django.urls import  reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, JsonResponse


class MedicosListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'shared.view_medicos'
    model = Medicos
    template_name = 'listas/list_medico.html'
    
    def get_queryset(self):
        # Utilizamos select_related para obtener los datos de tercero junto con Medicos
        return Medicos.objects.select_related('tercero').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.get_queryset())  # Verifica los datos cargados
        context['title'] = 'Listado de Medicos'
        context['entity'] = 'Medicos'
        context['Btn_Add'] = [
            {   
                'name': 'add',
                'label': 'Crear Medico',
                'icon': 'add',
                'url': 'configuracion:medicoscreate',
                'modal': 'Activar',
            }
        ]
        context['url_toggle'] = 'configuracion:estadopaquete'
        
        # Definir las cabeceras de la tabla
        context['headers'] = ['CEDULA', 'NOMBRES', 'APELLIDOS', 'COMISION %', 'DECUENTO %']
        context['fields'] = ['tercero__NumeroIdentificacion', 'tercero__Nombre', 'tercero__Apellido', 'comision', 'descuento']
        # Crear una lista de los datos que queremos mostrar
        data = [
            {
                'NumeroIdentificacion': medico.tercero.NumeroIdentificacion,
                'Nombres': medico.tercero.Nombre,
                'Apellidos': medico.tercero.Apellido,
                'comisiones': medico.comision,
                'descuentos': medico.descuento
            }
            for medico in self.get_queryset()
        ]
        
        # Asignar los datos al contexto
        context['data'] = data
        
        
        #
        # Definir las acciones disponibles para cada fila
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'white',
                'url': 'configuracion:medicosupdate',
                'modal': 'Activar'
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'configuracion:medicosdelete',
                'modal': 'Activar'
            },
        ]
        
        return context

class MedicosCreateView(CreateView):
    model = Medicos
    form_class = MedicosForm
    template_name = 'shared/create.html'
    success_url = reverse_lazy('configuracion:medicoslist')

    def form_valid(self, form):
        # guarda el medico
        medico = form.save()
        paquetes = form.cleaned_data.get('paquetes', [])
        
        # Asignar los paquetes al medico
        for paquete in paquetes:
            Medico_paquetes.objects.create(medico=medico, paquete=paquete)

        tercero = medico.tercero
        log_event(self.request.user, 'info', f'Se creó el médico {tercero.Nombre} {tercero.Apellido}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Medicos'
        context['entity'] = 'Medicos'
        context['action'] = 'add'
        context['list_url'] = self.success_url
        return context


class MedicosUpdateView(UpdateView):
    model = Medicos
    form_class = MedicosForm
    template_name = 'shared/create.html'
    success_url = reverse_lazy('configuracion:medicoslist')

    def get_initial(self):
        initial = super().get_initial()
        # Obtener los paquetes que ya están relacionados con el médico
        medico = self.object
        paquetes_seleccionados = Medico_paquetes.objects.filter(medico=medico).values_list('paquete', flat=True)
        # Asignar los paquetes al campo inicial del formulario
        initial['paquetes'] = paquetes_seleccionados
        return initial

    def form_valid(self, form):
        medico = form.save()
        paquetes = form.cleaned_data.get('paquetes', [])
        
        # Actualizar los paquetes del médico
        Medico_paquetes.objects.filter(medico=medico).delete()
        for paquete in paquetes:
            Medico_paquetes.objects.get_or_create(medico=medico, paquete=paquete)

        # Log the update event
        tercero = medico.tercero
        log_event(self.request.user, 'info', f'Se actualizó el médico {tercero.Nombre} {tercero.Apellido}')
        messages.success(self.request, f'Médico {tercero} actualizado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Medico'
        context['entity'] = 'Medicos'
        context['action'] = 'edit'
        context['list_url'] = self.success_url
        return context


class MedicosDeleteView(DeleteView):
    model = Medicos
    template_name = 'shared/del.html'
    success_url = reverse_lazy('configuracion:medicoslist')

    def delete(self, request, *args, **kwargs):
        medico = self.get_object()
        tercero = medico.tercero
        print(tercero)
        log_event(self.request.user, 'info', f'Eliminó al médico {tercero.Nombre} {tercero.Apellido}')
        messages.success(self.request, f'Se eliminó al médico {tercero.Nombre} {tercero.Apellido} con éxito.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tercero = self.object.tercero
        context['title'] = 'Eliminar Médico'
        context['entity'] = 'Médicos'
        context['texto'] = f'¿Está seguro de eliminar al médico {tercero.Nombre} {tercero.Apellido}?'
        context['list_url'] = reverse_lazy('configuracion:medicoslist')
        return context