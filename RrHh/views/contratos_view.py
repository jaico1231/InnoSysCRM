# from io import BytesIO
import os
from io import BytesIO
import re
from django.forms import BaseModelForm
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from weasyprint import HTML
from django.template.loader import render_to_string
from django import template
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View, TemplateView
from django.urls import reverse, reverse_lazy
from RrHh.forms import Contrato_LaboralForm
from RrHh.forms.contrato_laboral_form import  *
from RrHh.models.contrato_laboral import Contrato_Laboral, soportes_contrato
from RrHh.models.estado_contrato import estado_contrato
from shared.models.datos_empresa import DatosIniciales
from num2words import num2words
from django.template.loader import get_template

from django.shortcuts import get_object_or_404
from shared.global_utils import *
class PDFTemplateMixin:
    template_name = None

    # def render_to_pdf(self, context):
    #     template = get_template(self.template_name)
    #     html = template.render(context)
    #     response = HttpResponse(content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename="contrato.pdf"'
    #     pisa_status = pisa.CreatePDF(html, dest=response)
    #     if pisa_status.err:
    #         return HttpResponse(f'We had some errors <pre>{html}</pre>')
    #     return response

class Listar_Contratos(LoginRequiredMixin,  PermissionRequiredMixin,ListView):
    permission_required = 'RrHh.view_contrato_laboral'
    model = Contrato_Laboral
    # template_name = 'shared/list.html'
    template_name = 'Contratos/Listar_Contratos.html'
    form_class = Contrato_LaboralForm
    ##listar contratos en basic no carga el numero de cedula de la hoja de vida
    def get_queryset(self):
        # Usar select_related para evitar consultas adicionales al acceder a campos de relaciones
        queryset = super().get_queryset().select_related('hoja_vida_FK')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Contratos'
        context['entity'] = 'Contratos'
        context['add_url'] = reverse_lazy('administracion:Create_Tercero')
        context['headers'] = ['CONTRATO', 'DOCUMENTO', 'NOMBRE COMPLETO', 'CARGO', 'FECHA INICIO', 'FECHA FIN','TIPO CONTRATO','SALARIO','ESTADO']
        context['fields'] = ['id','hoja_vida_FK__numero_identificacion','hoja_vida_FK','cargo','fecha_inicio','fecha_fin','tipo_contratoFK','salario','estado_FK']
        context['actions'] = [
            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'RrHh:Editar_Contratos',
                # 'modal': '1'
            },
            {
                'name': 'print',
                'label': '',
                'icon': 'print',
                'color': 'success',
                'color2': 'white',
                'url': 'RrHh:detalle_contrato',
                'modal': '1'
            },
            {
                'name': 'novedad',
                'label': '',
                'icon': 'cancel_presentation',
                'color': 'warning',
                'color2': 'white',
                'url': 'RrHh:Novedad_Contrato',
                'modal': '1'
            }

        ]
        if self.request.user.groups.filter(name='Administrativos').exists():
            context['actions'].append(
                {
                    'name': 'delete',
                    'label': '',
                    'icon': 'delete',
                    'color': 'danger',
                    'color2': 'white',
                    'url': 'RrHh:Borrar_Contratos',
                    # 'modal': '1'
                }
            )

        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context
# class Listar_Contratos(LoginRequiredMixin, ListView):
#     model = Contrato_Laboral
#     template_name = 'shared/list.html'
#     form_class = Contrato_LaboralForm

#     def get_queryset(self):
#          # Usar select_related para evitar consultas adicionales al acceder a campos de relaciones
#          queryset = super().get_queryset().select_related('hoja_vida_FK', 'tipo_contratoFK', 'estado_FK')
#          for contrato in queryset:
#             print(f"Contrato ID: {contrato.id}")
#             print(f"Numero Identificacion: {contrato.hoja_vida_FK.numero_identificacion}")
#             print(f"Nombre: {contrato.hoja_vida_FK.nombre}")
#             print(f"Apellido: {contrato.hoja_vida_FK.apellido}")
            
#          return queryset
           
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Listar Contratos'
#         context['entity'] = 'Contratos'
#         context['add_url'] = reverse_lazy('RrHh:Crear_Contratos')
#         context['Btn_Add'] = [
#             {
#                 'url':'RrHh:Crear_Contratos',
#                 'modal': 'Activar',
#                 }
#         ]
#         context['headers'] = ['CONTRATO', 'DOCUMENTO', 'NOMBRE COMPLETO', 'CARGO', 'FECHA INICIO', 'FECHA FIN','TIPO CONTRATO','SALARIO','ESTADO']
#         queryset = super().get_queryset().select_related('hoja_vida_FK', 'tipo_contratoFK', 'estado_FK')
#         for contrato in queryset:
#             context['fields'] = ['id','contrato.hoja_vida_FK.numero_identificacion','hoja_vida_FK','cargo','fecha_inicio','fecha_fin','tipo_contratoFK','salario','estado_FK']
#         context['actions'] = [   
#             {
#                 'name': 'edit', 
#                 'label': '', 
#                 'icon': 'edit', 
#                 'color': 'secondary', 
#                 'color2': 'brown', 
#                 'url': 'RrHh:Editar_Contratos',
#                 'modal': '1'
#             },         
#             {
#                 'name': 'print', 
#                 'label': '', 
#                 'icon': 'visibility', 
#                 'color': 'success',
#                 'color2': 'white', 
#                 'url': 'RrHh:detalle_contrato',
#                 'modal': '1' 
#             },
#             {
#                 'name': 'novedad', 
#                 'label': '', 
#                 'icon': 'cancel_presentation', 
#                 'color': 'warning', 
#                 'color2': 'white', 
#                 'url': 'RrHh:Editar_Contratos',
#                 'modal': '1'
#             },
#         ]
#         if self.request.user.groups.filter(name='Administrativos').exists():
#             context['actions'].append(
#                 {
#                     'name': 'delete',
#                     'label': '',
#                     'icon': 'delete',
#                     'color': 'danger',
#                     'color2': 'white',
#                     'url': 'RrHh:Borrar_Contratos',
#                     'modal': '1'
#                 }
#             )
            
#         context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
#         return context


    
class Crear_Contratos(LoginRequiredMixin,  CreateView):
    permission_required = 'RrHh.add_contrato_laboral'
    form_class = Contrato_LaboralForm
    template_name = 'shared/create.html'
    
    def get_success_url(self):
        if self.request.is_ajax():
            return reverse_lazy('RrHh:Listar_Contratos')
        else:
            return reverse_lazy('RrHh:Listar_Contratos')
        

    def form_valid(self, form):
        response = super().form_valid(form)
        log_event(self.request.user, 'info', f'Se agrego correctamente el Contrato. {form.instance}')
        if self.request.is_ajax():
            return JsonResponse({'success': True})
        return response

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Contratos'
        context['entity'] = 'Contratos'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context
  
class Editar_Contratos(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'RrHh.change_contrato_laboral'
    model = Contrato_Laboral
    form_class = Contrato_LaboralForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('RrHh:Listar_Contratos')
    
          

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Contratos'
        context['entity'] = 'Contratos'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context
    
class Borrar_Contratos(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'RrHh.delete_contrato_laboral'
    model = Contrato_Laboral
    template_name = 'Contratos/Borrar_Contratos.html'
    success_url = reverse_lazy('RrHh:Listar_Contratos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Contratos'
        context['entity'] = 'Contratos'
        context['texto'] = f'¿Estás seguro de que deseas eliminar el Contrato {self.object.id}?'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context

class Detalle_Contratos(LoginRequiredMixin, PermissionRequiredMixin, PDFTemplateMixin, DetailView):
    permission_required = 'RrHh.view_contrato_laboral'
    model = Contrato_Laboral
    template_name = 'cartas/Contrato_Laboral.html'
    
    def get_object(self, pk):
        return get_object_or_404(Contrato_Laboral, pk=pk)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs['pk'])
        numero_identificacion = self.object.hoja_vida_FK.numero_identificacion
        doc = f'Contrato_Laboral_{self.object.id}.pdf'
        ruta = f'DOCUMENTOS/{numero_identificacion}/CONTRATO/{doc}'
        ruta_completa = f"/ROMIL_BETA1/ROMIL_BETA1/static/assets/{ruta}"
        os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
        context = self.get_context_data()
        template = get_template('cartas/Contrato_Laboral copy.html')
        html_template = template.render(context)
        HTML(string=html_template).write_pdf(ruta_completa)
        return FileResponse(open(ruta_completa, 'rb'), as_attachment=True, filename=doc)

        
        # Para la demostración, estamos imprimiendo la información en consola
        # Puedes descomentar la siguiente línea para generar el PDF
        # self.generate_pdf(ruta)

        
        context = self.get_context_data()
        return render(request, self.template_name, context)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contrato = self.object
        iniciales = DatosIniciales.objects.get(id=1)
        try:
            salario_numerico = float(contrato.salario)
        except ValueError:
            salario_numerico = 0.0
        salario_formateado = "${:,.2f}".format(salario_numerico).replace(',', ' ').replace('.', ',').replace(' ','.')
        salario_texto = num2words(salario_numerico, lang='es').upper()
        dia_en_letras = num2words(contrato.fecha_inicio.day, lang='es').capitalize()
        mes_en_letras = mes_en_letras_espanol(contrato.fecha_inicio.strftime('%B'))
        anio_en_letras = num2words(contrato.fecha_inicio.year, lang='es').capitalize()
        context['iniciales'] = iniciales
        context['salario_texto'] = salario_texto
        context['salario_formateado'] = salario_formateado
        context['id_contrato'] = contrato.id
        context['dia_en_letras'] = dia_en_letras
        context['mes_en_letras'] = mes_en_letras
        context['anio_en_letras'] = anio_en_letras
        context['title'] = 'Contratos'
        context['entity'] = 'Contratos'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context
    
    def PDF(self, request, *args, **kwargs):
        self.object = self.get_object()
        identificacion = self.object.hoja_vida.numero_identificacion
        
class NovedadContratoView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'RrHh.add_contrato_laboral'
    template_name = 'Contratos/novedad_contrato.html'
    model = Contrato_Laboral

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novedad Contrato'
        context['entity'] = 'Novedad'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        context['renuncia_form'] = RenunciaForm()
        context['despido_form'] = DespidoForm()
        return context

    def post(self, request, *args, **kwargs):
        renuncia_form = RenunciaForm(request.POST, request.FILES)
        despido_form = DespidoForm(request.POST)
        if renuncia_form.is_valid():
            renuncia_form.instance.estado_FK = estado_contrato.objects.get(id=3)
            renuncia_form.instance.user_updated = self.request.user
            user_update = self.request.user
            renuncia_form.instance.user_updated = user_update        
            context = self.get_context_data()
            dia_en_letras = num2words(self.object.fecha_notificacion_renuncia.day, lang='es').capitalize()
            mes_en_letras = mes_en_letras_espanol(self.object.fecha_notificacion_renuncia.strftime('%B'))
            anio_en_letras = num2words(self.object.fecha_notificacion_renuncia.year, lang='es').capitalize()
            dia_en_letras_efectiva = num2words(self.object.fecha_renuncia.day, lang='es').capitalize()
            mes_en_letras_efectiva = mes_en_letras_espanol(self.object.fecha_renuncia.strftime('%B'))
            anio_en_letras_efectiva = num2words(self.object.fecha_renuncia.year, lang='es').capitalize()        
            context['dia_en_letras'] = dia_en_letras
            context['mes_en_letras'] = mes_en_letras
            context['anio_en_letras'] = anio_en_letras
            context['mes_en_letras_efectiva'] = mes_en_letras_efectiva
            context['anio_en_letras_efectiva'] = anio_en_letras_efectiva
            context['dia_en_letras_efectiva'] = dia_en_letras_efectiva
            numero_identificacion = renuncia_form.instance.hoja_vida_FK.numero_identificacion
            numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
            doc = f'Aceptacion_Renuncia_{numero_identificacion}.pdf'
            ruta = f'DOCUMENTOS/{numero_identificacion}/RENUNCIA/{doc}'  # Asegúrate de definir correctamente la variable 'doc'
            ruta_completa = f"/ROMIL_BETA1/ROMIL_BETA1/static/assets/{ruta}"
            renuncia_form.instance.carta_renuncia = ruta_completa
            renuncia_form.save()
            os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
            template = get_template('cartas/Carta_Aceptacion_Renuncia_Voluntaria.html')
            html_template = template.render(context)
            HTML(string=html_template).write_pdf(target=ruta_completa)
            renuncia_form.save()
        elif despido_form.is_valid():
            despido_form = DespidoForm(request.POST)
            despido_form.estado_FK = 3
            despido_form.save()
        log_event(self.request.user, "info", f"Se finalizo el Contrato. {self.object}")
        
        return render(request, self.template_name, self.get_context_data())

class  Renuncia(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'RrHh.change_contrato_laboral'
    model = Contrato_Laboral
    form_class = RenunciaForm
    template_name = 'Contratos/Crear_contrato.html'
    success_url = reverse_lazy('RrHh:Listar_Contratos')

    def form_valid(self, form):
        form.instance.estado_FK = estado_contrato.objects.get(id=3)
        form.instance.user_updated = self.request.user
        user_update = self.request.user
        form.instance.user_updated = user_update        
        context = self.get_context_data()
        dia_en_letras = num2words(self.object.fecha_notificacion_renuncia.day, lang='es').capitalize()
        mes_en_letras = mes_en_letras_espanol(self.object.fecha_notificacion_renuncia.strftime('%B'))
        anio_en_letras = num2words(self.object.fecha_notificacion_renuncia.year, lang='es').capitalize()
        dia_en_letras_efectiva = num2words(self.object.fecha_renuncia.day, lang='es').capitalize()
        mes_en_letras_efectiva = mes_en_letras_espanol(self.object.fecha_renuncia.strftime('%B'))
        anio_en_letras_efectiva = num2words(self.object.fecha_renuncia.year, lang='es').capitalize()        
        context['dia_en_letras'] = dia_en_letras
        context['mes_en_letras'] = mes_en_letras
        context['anio_en_letras'] = anio_en_letras
        context['mes_en_letras_efectiva'] = mes_en_letras_efectiva
        context['anio_en_letras_efectiva'] = anio_en_letras_efectiva
        context['dia_en_letras_efectiva'] = dia_en_letras_efectiva
        numero_identificacion = form.instance.hoja_vida_FK.numero_identificacion
        numero_identificacion = re.sub(r'\W+', '_', str(numero_identificacion))
        doc = f'Aceptacion_Renuncia_{numero_identificacion}.pdf'
        ruta = f'DOCUMENTOS/{numero_identificacion}/RENUNCIA/{doc}'  # Asegúrate de definir correctamente la variable 'doc'
        ruta_completa = f"/ROMIL_BETA1/ROMIL_BETA1/static/assets/{ruta}"
        form.instance.carta_renuncia = ruta_completa
        form.save()
        os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
        template = get_template('cartas/Carta_Aceptacion_Renuncia_Voluntaria.html')
        html_template = template.render(context)
        HTML(string=html_template).write_pdf(target=ruta_completa)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        iniciales = DatosIniciales.objects.get(id=1)
        context['iniciales'] = iniciales
        context['title'] = 'Renuncia Notificada'
        context['entity'] = 'Novedad'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context
    
class Despido(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'RrHh.change_contrato_laboral'
    model = Contrato_Laboral
    form_class = DespidoForm
    template_name = 'Contratos/Crear_contrato.html'
    success_url = reverse_lazy('RrHh:Listar_Contratos')
    
    def post(self, request, *args, **kwargs):
        despido_form = DespidoForm(request.POST)
        despido_form.estado_FK = 3
        despido_form.save()
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Despido Justificado'
        context['entity'] = 'Novedad'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context
    
class Anexo_Contrato(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'RrHh.change_contrato_laboral'
    model = Contrato_Laboral
    form_class = Anexo_ContratoForm
    template_name = 'Contratos/anexos.html'
    
    def dispatch(self, *args, **kwargs):
        self.contrato = get_object_or_404(Contrato_Laboral, pk=self.kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('RrHh:Anexo_Contrato', kwargs={'pk': self.contrato.pk})

    def form_valid(self, form):
        soportes_contrato.objects.create(
            Contrato_Laboral_FK=Contrato_Laboral.objects.get(pk=self.contrato.pk),
            nombre_soporte=form.cleaned_data.get('nombre_soporte'),
            soporte=form.cleaned_data.get('soporte'),
            user_created=self.request.user
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = soportes_contrato.objects.filter(Contrato_Laboral_FK=self.contrato)
        context['formulario'] = self.get_form()
        context['lista'] = lista
        for x in context['lista']:
            x.nombre_archivo = os.path.basename(x.soporte.name)
            print (x.soporte)
        context['title'] = 'Anexo Contrato'
        context['entity'] = 'Novedad'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context
    
class crear_soportes(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'RrHh.add_contrato_laboral'
    model = soportes_contrato
    form_class = Anexo_ContratoForm
    template_name = 'Contratos/anexos.html'
    success_url = reverse_lazy('RrHh:Listar_Contratos')

    def form_valid(self, form):
        form.instance.Contrato_Laboral_FK = Contrato_Laboral.objects.get(pk=self.kwargs['pk'])
        form.instance.user_created = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista'] = soportes_contrato.objects.all().filter(Contrato_Laboral_FK=self.kwargs['pk'])  # Ajusta esto según tus necesidades
        for x in context['lista']:
            x.nombre_archivo = os.path.basename(x.soporte.name)
            print (x.soporte)
        context['title'] = 'Anexo Contrato'
        context['entity'] = 'Novedad'
        context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
        return context