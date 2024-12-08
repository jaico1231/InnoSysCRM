
import os
from io import BytesIO
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.conf import settings
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from weasyprint import HTML
from shared.models.genero import Sexo
from shared.models.tipo_documento import Tipo_Documento
from shared.models.geografia import *
from RrHh.forms.hoja_vida_form import *
from RrHh.forms.grupo_familiar_form import Grupo_FamiliarForm
from RrHh.forms.educacion_form import EducacionForm
from RrHh.forms.experiencia_laboral_form import ExperienciaForm
from RrHh.models.hoja_vida import Hoja_Vida
from RrHh.models.grupo_familiar import Grupo_Familiar
from RrHh.models.educacion import Educacion
from RrHh.models.experiencia_laboral import experiencia_laboral
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import get_template
from RrHh.models.llamado_atencion import Descargos, Llamado_Atencion
from django.utils import timezone

from shared.loggin import log_event


class Listar_Hoja_Vida(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'RrHh.view_hoja_vida'
    model = Hoja_Vida
    template_name = 'HV/listar_HV.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Hoja de Vida'
        context['entity'] = 'Hoja de Vida'
        context['add_url'] = reverse_lazy('RrHh:Crear_HV')
        context['headers'] = ['ID', 'NOMBRE', 'APELLIDO', 'DOCUMENTO', 'CORREOS', 'TELEFONO']
        context['fields'] = ['IdHojaVida', 'nombre', 'apellido', 'numero_identificacion', 'email', 'telefono']
        context['actions'] = [            
            {
                'name': 'print', 
                'label': '', 
                'icon': 'visibility', 
                'color': 'success',
                'color2': 'white', 
                'url': 'RrHh:Detalle_HV',
                'modal': '1' # 
            },
            {
                'name': 'edit', 
                'label': '', 
                'icon': 'edit', 
                'color': 'secondary', 
                'color2': 'brown', 
                'url': 'RrHh:Editar_HV',
                'modal': '1'
            },          
            
            
            # Agrega más acciones aquí sea necesario
        ]
        if self.request.user.groups.filter(name='Administrativos').exists():
            context['actions'].append(
                {
                    'name': 'delete',
                    'label': '',
                    'icon': 'delete',
                    'color': 'danger',
                    'color2': 'white',
                    'url': 'RrHh:Borrar_HV',
                    # 'modal': '1'
                }
            )
        
        return context

class Detalle_Hoja_Vida(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'RrHh.view_hoja_vida'
    template_name = 'HV/HV.html'
    form_class=HojaVidaForm
    def post(self, request, *args, **kwargs):
        if 'print' in request.POST:
            context = self.get_context_data()
            template = get_template('HV/HV_Exp.html')
            html_template = template.render(context)
            
            pdf_buffer = BytesIO()
            HTML(string=html_template).write_pdf(pdf_buffer)
            pdf_buffer.seek(0)

            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Hoja_de_Vida.pdf"'
            return response
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hojas_de_vida = Hoja_Vida.objects.all().filter(pk=self.kwargs['pk']).first()
        Lista_Grupo_Familiar = Grupo_Familiar.objects.all().filter(empleado_FK=self.kwargs['pk'])
        Lista_Educacion = Educacion.objects.all().filter(hoja_vida_FK=self.kwargs['pk'])
        Lista_Experiencia = experiencia_laboral.objects.all().filter(hoja_vida_FK=self.kwargs['pk'])
        Llamados_Atencion = Llamado_Atencion.objects.all().filter(colaborador=hojas_de_vida.IdHojaVida)
        context['Lista_GF'] = Lista_Grupo_Familiar
        context['Lista_EDUC'] = Lista_Educacion
        context['Lista_EXP'] = Lista_Experiencia
        context['Lista_Ll_Aten'] = Llamados_Atencion
        context['hojas_de_vida'] = hojas_de_vida
        context['title'] = 'Hoja de Vida'
        context['entity'] = 'Hoja de Vida'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
    
class Crear_Hoja_Vida(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'RrHh.add_hoja_vida'
    form_class = HojaVidaForm
    template_name = 'HV/Crear_HV.html'

    def get_success_url(self):
        # if self.request.accepts('application/json'):
        #     return JsonResponse({'success': True})
        # else:
        return reverse_lazy('RrHh:Listar_HV')
        
    def form_valid(self, form):
        form.save()
        if self.request.method == 'POST':
            form = Grupo_FamiliarForm(self.request.POST, self.request.FILES)
            validar = self.request.POST.get('nombre_GF')
            if validar != '':
                nombre = self.request.POST.getlist('nombre_GF')
                apellido = self.request.POST.getlist('apellido_GF')
                parentesco = self.request.POST.getlist('parentesco_GF')
                sexo = self.request.POST.getlist('sexo_FK_GF')                
                fecha_nacimiento = self.request.POST.getlist('fecha_nacimiento_GF')
                tipo_documento = self.request.POST.getlist('tipo_documento_GF')
                numero_identificacion = self.request.POST.getlist('numero_identificacion_GF')
                
                empleado_FK=Hoja_Vida.objects.get(pk=self.object.pk)
                
                for i in range(len(nombre)):
                    
                    Grupo_Familiar.objects.create(
                        nombre_GF=nombre[i],
                        apellido_GF=apellido[i],
                        parentesco_GF=parentesco[i],
                        tipo_documento_GF=Tipo_Documento.objects.get(IdTipoDoc=tipo_documento[i]),
                        sexo_FK_GF = Sexo.objects.get(IdSexo=sexo[i]),
                        fecha_nacimiento_GF=fecha_nacimiento[i],
                        numero_identificacion_GF=numero_identificacion[i],
                        empleado_FK=empleado_FK,
                        user_created = self.request.user                    
                    )
                    log_event(self.request.user, 'info', f'Se agrego correctamente el familiar {nombre[i]}.')

        if self.request.method == 'POST':
            form = EducacionForm(self.request.POST, self.request.FILES)
            validar = self.request.POST.get('institucion_EDU')
            if validar != '':
                institucion = self.request.POST.getlist('institucion_EDU')
                titulo = self.request.POST.getlist('titulo_EDU')
                duracion = self.request.POST.getlist('duracion_EDU')
                unidad = self.request.POST.getlist('TextoUnidad_EDU')
                pais = self.request.POST.getlist('pais_EDU')
                fecha_inicio = self.request.POST.getlist('fecha_inicio_EDU')
                fecha_fin = self.request.POST.getlist('fecha_fin_EDU')                
                user_created = self.request.user
                hoja_vida_FK=Hoja_Vida.objects.get(pk=self.object.pk)

                for i in range(len(institucion)):
                    
                    Educacion.objects.create(
                        institucion_EDU = institucion[i],
                        titulo_EDU = titulo[i],
                        duracion_EDU = duracion[i],
                        fecha_inicio_EDU = fecha_inicio[i],
                        fecha_fin_EDU = fecha_fin[i],
                        pais_EDU = Paises.objects.get(IdPais=(pais[i])),
                        TextoUnidad_EDU = unidad[i],
                        # user_created = self.request.user,
                        hoja_vida_FK=hoja_vida_FK
                    )
                    log_event(self.request.user, 'info', f'Se agrego correctamente la Educacion {institucion[i]}.')

        if self.request.method == 'POST':
            form = ExperienciaForm(self.request.POST, self.request.FILES)
            validar = self.request.POST.get('cargo_EXP')
            if validar != '':
                hoja_vida_FK=Hoja_Vida.objects.get(pk=self.object.pk)
                cargo = self.request.POST.getlist('cargo_EXP')
                empresa = self.request.POST.getlist('empresa_EXP')
                fecha_inicio = self.request.POST.getlist('fecha_inicio_EXP')
                fecha_fin = self.request.POST.getlist('fecha_fin_EXP')

                for i in range(len(cargo)):                    
                    experiencia_laboral.objects.create(
                        cargo_EXP = cargo[i],
                        empresa_EXP = empresa[i],
                        fecha_inicio_EXP = fecha_inicio[i],
                        fecha_fin_EXP = fecha_fin[i],
                        hoja_vida_FK=hoja_vida_FK
                    )
                    log_event(self.request.user, 'info', f'Se agrego correctamente la Experiencia laboral {cargo[i]}.')
        
        log_event(self.request.user, 'info', f'Se Creo correctamente la Hoja de Vida. {self.object}')
        return super().form_valid(form)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        GF_Form = Grupo_FamiliarForm()
        Educacion_Form = EducacionForm()
        Experiencia_Form = ExperienciaForm()
        context['GF_FORM'] = GF_Form
        context['EDUC_FORM'] = Educacion_Form
        context['EXP_FORM'] = Experiencia_Form
        context['title'] = 'Crear Hoja de Vida'
        context['entity'] = 'Hoja de Vida'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
 
class Editar_Hoja_Vida(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'RrHh.change_hoja_vida'
    model = Hoja_Vida
    form_class = HojaVida_UpdateForm
    # form_class = Hoja_Vida_Form2
    template_name = 'HV/Editar_HV.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('RrHh:Listar_HV')

    def form_valid(self, form):
        form.save()
        if self.request.method == 'POST':
            form = Grupo_FamiliarForm(self.request.POST, self.request.FILES)
            validar = self.request.POST.get('nombre_GF')
            if validar != '':
                nombre = self.request.POST.getlist('nombre_GF')
                apellido = self.request.POST.getlist('apellido_GF')
                parentesco = self.request.POST.getlist('parentesco_GF')
                sexo = self.request.POST.getlist('sexo_FK_GF')                
                fecha_nacimiento = self.request.POST.getlist('fecha_nacimiento_GF')
                tipo_documento = self.request.POST.getlist('tipo_documento_GF')
                numero_identificacion = self.request.POST.getlist('numero_identificacion_GF')
                
                empleado_FK=Hoja_Vida.objects.get(pk=self.object.pk)
                
                for i in range(len(nombre)):
                    
                    Grupo_Familiar.objects.create(
                        nombre_GF=nombre[i],
                        apellido_GF=apellido[i],
                        parentesco_GF=parentesco[i],
                        tipo_documento_GF=Tipo_Documento.objects.get(IdTipoDoc=tipo_documento[i]),
                        sexo_FK_GF = Sexo.objects.get(IdSexo=sexo[i]),
                        fecha_nacimiento_GF=fecha_nacimiento[i],
                        numero_identificacion_GF=numero_identificacion[i],
                        empleado_FK=empleado_FK,
                        user_created = self.request.user                    
                    )
                    log_event(self.request.user, 'info', f'Se agrego correctamente el grupo familiar {nombre[i]}.')

        if self.request.method == 'POST':
            form = EducacionForm(self.request.POST, self.request.FILES)
            validar = self.request.POST.get('institucion_EDU')
            if validar != '':
                institucion = self.request.POST.getlist('institucion_EDU')
                titulo = self.request.POST.getlist('titulo_EDU')
                duracion = self.request.POST.getlist('duracion_EDU')
                unidad = self.request.POST.getlist('TextoUnidad_EDU')
                pais = self.request.POST.getlist('pais_EDU')
                fecha_inicio = self.request.POST.getlist('fecha_inicio_EDU')
                fecha_fin = self.request.POST.getlist('fecha_fin_EDU')                
                user_created = self.request.user
                hoja_vida_FK=Hoja_Vida.objects.get(pk=self.object.pk)

                for i in range(len(institucion)):
                    
                    Educacion.objects.create(
                        institucion_EDU = institucion[i],
                        titulo_EDU = titulo[i],
                        duracion_EDU = duracion[i],
                        fecha_inicio_EDU = fecha_inicio[i],
                        fecha_fin_EDU = fecha_fin[i],
                        pais_EDU = Paises.objects.get(IdPais=(pais[i])),
                        TextoUnidad_EDU = unidad[i],
                        # user_created = self.request.user,
                        hoja_vida_FK=hoja_vida_FK
                    )
                    log_event(self.request.user, 'info', f'Se agrego correctamente la educacion {institucion[i]}.')

        if self.request.method == 'POST':
            form = ExperienciaForm(self.request.POST, self.request.FILES)
            validar = self.request.POST.get('cargo_EXP')
            if validar != '':
                hoja_vida_FK=Hoja_Vida.objects.get(pk=self.object.pk)
                cargo = self.request.POST.getlist('cargo_EXP')
                empresa = self.request.POST.getlist('empresa_EXP')
                fecha_inicio = self.request.POST.getlist('fecha_inicio_EXP')
                fecha_fin = self.request.POST.getlist('fecha_fin_EXP')

                for i in range(len(cargo)):                    
                    experiencia_laboral.objects.create(
                        cargo_EXP = cargo[i],
                        empresa_EXP = empresa[i],
                        fecha_inicio_EXP = fecha_inicio[i],
                        fecha_fin_EXP = fecha_fin[i],
                        hoja_vida_FK=hoja_vida_FK
                    )
                    log_event(self.request.user, 'info', f'Se agrego correctamente la experiencia laboral {cargo[i]}.')
        log_event(self.request.user, 'info', f'Se actualizo correctamente la hoja de vida. {self.object}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        
        context['id'] = self.object.pk

        # Obtain lists of Family Group, Education, and Work Experience
        Lista_Grupo_Familiar = Grupo_Familiar.objects.filter(empleado_FK=id)
        
        Lista_Educacion = Educacion.objects.filter(hoja_vida_FK=id)
        Lista_Experiencia = experiencia_laboral.objects.filter(hoja_vida_FK=id)     
        context['Lista_GF'] = Lista_Grupo_Familiar
        context['Lista_EDUC'] = Lista_Educacion
        context['Lista_EXP'] = Lista_Experiencia

        GF_Form = Grupo_FamiliarForm()
        Educacion_Form = EducacionForm()
        Experiencia_Form = ExperienciaForm()
        context['GF_FORM'] = GF_Form
        context['EDUC_FORM'] = Educacion_Form
        context['EXP_FORM'] = Experiencia_Form

        context['title'] = 'Actualizar Hoja de Vida'
        context['entity'] = 'Hoja de Vida'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_HV')

        # Other context data assignments...

        return context
    def load_modal_content(request):
        template_name = request.GET.get('template')
        context = {}  # Agrega cualquier contexto adicional si es necesario
        
        html_content = render_to_string(template_name, context, request=request)
        return JsonResponse({'html_content': html_content})

class Borrar_Hoja_Vida(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'RrHh.delete_hoja_vida'
    model = Hoja_Vida
    template_name = 'shared/del.html'
    
    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('RrHh:Listar_HV')
        
    def form_valid(self, form):
        log_event(self.request.user, 'info', f'Se elimino correctamente la hoja de vida. {self.object}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print ('Ingresamos a borrar pero no funciona')
        context['title'] = 'Borrar Hoja de Vida'
        context['entity'] = 'Hoja de Vida'
        context['texto'] = f'¿Estás seguro de que deseas eliminar la Hoja de Vida de {self.object.nombre} {self.object.apellido}?'
        context['list_url'] = reverse_lazy('RrHh:Listar_HV')
        return context
  
class Contrato_pdf(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        detalle_contratos_view = Detalle_Hoja_Vida()  # Assuming DetalleContratos is a valid view
        context = {}
        pdf_content = detalle_contratos_view.render_to_pdf(context=context).content  # Assuming render_to_pdf() returns the PDF content
        pdf_file = HTML(string=pdf_content).write_pdf()  # Generate the PDF file
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="contrato.pdf"'
        return response