from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from Contabilidad.models.nomina import *
from Contabilidad.models.retroactivo import *
from Contabilidad.forms.novedades import*
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import JsonResponse
from Contabilidad.models.nomina import *
from Contabilidad.models.retroactivo import *
from Contabilidad.models.conceptos import *
from Contabilidad.forms.novedades import UploadCSVForm  # Asumiendo que tienes un formulario para cargar el CSV
import csv
from MacroProcesos.models.horarios_cargos import Horario_cargos

class ProcesarNovedadesNominaView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = ('Contabilidad.view_novedadesnomina', 'Contabilidad.add_novedadesnomina', 'Contabilidad.change_novedadesnomina', 'Contabilidad.delete_novedadesnomina')
    template_name = 'procesar_novedades_nomina.html'
    form_class = UploadCSVForm
    success_url = reverse_lazy('procesar_novedades_nomina')

    def form_valid(self, form):
        # Paso 1: Cargar archivo CSV con el listado de asistencia
        csv_file = form.cleaned_data['file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Asistencia.objects.create(
                empleado=row['empleado'],
                fecha=row['fecha'],
                entrada=row['entrada'],
                salida=row['salida']
            )

        # Paso 2: Cruzar el listado de asistencia con los Horario_cargos
        asistencias = Asistencia.objects.all()
        novedades = []

        for asistencia in asistencias:
            try:
                horario = Horario_cargos.objects.get(cargo=asistencia.empleado)
                entrada = asistencia.entrada
                salida = asistencia.salida

                # Calcular horas extras
                horas_extras = self.calcular_horas_extras(horario, entrada, salida)

                # Paso 4: Cruzar los datos y separar las horas extras del horario laboral
                novedad = NovedadNomina(
                    contrato=asistencia.empleado,
                    asistencias=asistencia,
                    horas_extra_normal=horas_extras['horas_extra_normal'],
                    horas_extra_nocturna=horas_extras['horas_extra_nocturna'],
                    horas_extra_dominical_diurna=horas_extras['horas_extra_dominical_diurna'],
                    horas_extra_dominical_nocturna=horas_extras['horas_extra_dominical_nocturna'],
                    horas_extra_festivo_diurno=horas_extras['horas_extra_festivo_diurno'],
                    horas_extra_festivo_nocturno=horas_extras['horas_extra_festivo_nocturno'],
                    horas_permiso_laboral=horas_extras['horas_permiso_laboral'],
                    horas_llegada_tarde=horas_extras['horas_llegada_tarde']
                )

                # Paso 5: Sumar el auxilio no prestacional
                auxilios = AuxilioNoPrestacional.objects.filter(contrato=asistencia.empleado)
                total_auxilio = sum(auxilio.valor for auxilio in auxilios)

                # Paso 6: Sumar el rodamiento no prestacional
                rodamientos = RodamNoPresta.objects.filter(contrato=asistencia.empleado)
                total_rodamiento = sum(rodamiento.valor for rodamiento in rodamientos)

                # Paso 7: Restar los descuentos mensuales
                descuentos = DescuentoAdicional.objects.filter(contrato=asistencia.empleado)
                total_descuento = sum(descuento.valor for descuento in descuentos)

                novedad.total_auxilio = total_auxilio
                novedad.total_rodamiento = total_rodamiento
                novedad.total_descuento = total_descuento

                novedades.append(novedad)

            except Horario_cargos.DoesNotExist:
                continue

        NovedadNomina.objects.bulk_create(novedades)
        return JsonResponse({"status": "success"})

    def calcular_horas_extras(self, horario, entrada, salida):
        # Implementar la lógica de cálculo de horas extras aquí
        horas_extra_normal = 0
        horas_extra_nocturna = 0
        horas_extra_dominical_diurna = 0
        horas_extra_dominical_nocturna = 0
        horas_extra_festivo_diurno = 0
        horas_extra_festivo_nocturno = 0
        horas_permiso_laboral = 0
        horas_llegada_tarde = 0

        # Lógica de cálculo de horas extras basada en la entrada y salida
        # ...
        return {
            'horas_extra_normal': horas_extra_normal,
            'horas_extra_nocturna': horas_extra_nocturna,
            'horas_extra_dominical_diurna': horas_extra_dominical_diurna,
            'horas_extra_dominical_nocturna': horas_extra_dominical_nocturna,
            'horas_extra_festivo_diurno': horas_extra_festivo_diurno,
            'horas_extra_festivo_nocturno': horas_extra_festivo_nocturno,
            'horas_permiso_laboral': horas_permiso_laboral,
            'horas_llegada_tarde': horas_llegada_tarde
        }


class NovedadNominaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('contabilidad.view_novedadnomina',)
    model = NovedadNomina
    template_name = 'shared/list.html'

class NovedadNominaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = NovedadNomina
    form_class = NovedadNominaForm
    template_name = 'contabilidad/novedad_nomina_form.html'
    success_url = reverse_lazy('contabilidad:novedad_nomina_list')

class NovedadNominaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = NovedadNomina
    form_class = NovedadNominaForm
    template_name = 'contabilidad/novedad_nomina_form.html'
    success_url = reverse_lazy('contabilidad:novedad_nomina_list')

class NovedadNominaDeleteView(DeleteView):
    model = NovedadNomina
    template_name = 'contabilidad/novedad_nomina_confirm_delete.html'
    success_url = reverse_lazy('contabilidad:novedad_nomina_list')

# Repeat similar class-based views for other models...
