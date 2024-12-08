from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from RrHh.models.permiso_laboral import Permiso_Laboral
from RrHh.views.carta_view import *
from RrHh.views.contratos_view import *
from RrHh.views.descargos_view import *
from RrHh.views.hoja_vida_view import *
from RrHh.views.datos_dashboard import *
from RrHh.views.grupo_familiar_view import *
from RrHh.views.educacion_view import *
from RrHh.views.experiencia_laboral_view import *
from RrHh.views.generar_cartas import Generar_Carta
from RrHh.views.permiso_laboralView import *
from RrHh.views.gestion_vacaciones import *
from RrHh.views.llamado_atencion import *
from django.contrib.auth.decorators import login_required
from ROMIL_BETA1.urls import add_menu_name
app_name='RrHh'
urlpatterns = [
    
    path('RrHh/', login_required(add_menu_name('HOJA DE VIDA')(Listar_Hoja_Vida.as_view())), name='Listar_HV'),
    path('RrHh/<int:pk>/', login_required(Detalle_Hoja_Vida.as_view()), name='Detalle_HV'),
    path('RrHh/edit/<int:pk>/', login_required(Editar_Hoja_Vida.as_view()), name='Editar_HV'),
    path('RrHh/add', login_required(Crear_Hoja_Vida.as_view()), name='Crear_HV'),
    path('RrHh/delete/<int:pk>/', login_required(Borrar_Hoja_Vida.as_view()), name='Borrar_HV'),
    path('RrHh/details/historial/<int:pk>/', login_required(Historial_Llamado_Atencion.as_view()), name='Historial_HV'),
    ############################################################################################
    
    path('RrHh/contratos/', login_required(add_menu_name('CONTRATOS')(Listar_Contratos.as_view())), name='Listar_Contratos'),
    path('RrHh/contratos/edit/<int:pk>/', login_required(Editar_Contratos.as_view()), name='Editar_Contratos'),
    path('RrHh/contratos/add/', login_required(Crear_Contratos.as_view()), name='Crear_Contratos'),
    path('RrHh/contratos/delete/<int:pk>/', login_required(Borrar_Contratos.as_view()), name='Borrar_Contratos'),
    path('RrHh/contratos/details/<int:pk>/', login_required(Detalle_Contratos.as_view()), name='detalle_contrato'),
    path('RrHh/contratos/novedad/<int:pk>/', login_required(NovedadContratoView.as_view()), name='Novedad_Contrato'),
    path('RrHh/contratos/renuncia/<int:pk>/', login_required(Renuncia.as_view()), name='Renuncia_Contrato'),#Contrato_Laboral
    path('RrHh/contratos/despido/<int:pk>/', login_required(Despido.as_view()), name='Despido_Contrato'),
    path('RrHh/contrato/docs/<int:pk>/', login_required(Anexo_Contrato.as_view()), name='Anexo_Contrato'),
        
    ############################################################################################
    path('RrHh/contratos/listar_GF', login_required(add_menu_name('GRUPO FAMILIAR')(Listar_Grupo_Familiar.as_view())), name='Listar_GF'),
    path('RrHh/contratos/add_GF', login_required(Crear_Grupo_Familiar.as_view()), name='Crear_GF'),
    path('RrHh/contratos/edit_GF/<int:pk>/', login_required(Editar_Grupo_Familiar.as_view()), name='Editar_GF'),
    path('RrHh/contratos/delete_GF/<int:pk>/', login_required(Borrar_Grupo_Familiar.as_view()), name='Borrar_GF'),
    
    ############################################################################################

    path('RrHh/contratos/add_EDU', login_required(Crear_Educacion.as_view()), name='Crear_EDU'),
    path('RrHh/contratos/edit_EDU/<int:pk>/', login_required(Editar_Educacion.as_view()), name='Editar_EDU'),
    path('RrHh/contratos/delete_EDU/<int:pk>/', login_required(Borrar_Educacion.as_view()), name='Borrar_EDU'),

    ############################################################################################

    path('RrHh/contratos/add_EXP', login_required(Crear_Experiencia_Laboral.as_view()), name='Crear_EXP'),
    path('RrHh/contratos/edit_EXP/<int:pk>/', login_required(Editar_Experiencia_Laboral.as_view()), name='Editar_EXP'),
    path('RrHh/contratos/delete_EXP/<int:pk>/', login_required(Borrar_Experiencia_Laboral.as_view()), name='Borrar_EXP'),
    

    ############################################################################################
    path('RrHh/sp/list', login_required(add_menu_name('PERMISOS')(Listar_Solicitudes_Permiso.as_view())), name='Listar_Solicitudes_Permisos'),#Listar_Solicitudes
    path('RrHh/sp/add', login_required(Crear_Permiso_Laboral.as_view()), name='Crear_Solicitud_permiso_laboral'),
    path('RrHh/sp/edit/<int:pk>/', login_required(Permiso_Laboral_Edit.as_view()), name='Editar_Solicitud_permiso_laboral'),
    path('RrHh/sp/delete/<int:pk>/', login_required(Permiso_Laboral_Delete.as_view()), name='Borrar_Solicitud_permiso_laboral'),
    path('RrHh/sp/history/<int:pk>/', login_required(Historial_Permiso_Laboral.as_view()), name='Historial_SP'),
    path('RrHh/sp/print/<int:pk>/', login_required(Imprimir_Permiso_Laboral.as_view()), name='imprimir_SP'),
    # LLAMADOS DE ATENCION
    ############################################################################################
    path('RrHh/llamado_atencion/list', login_required(add_menu_name('LLAMADOS DE ATENCION')(Listar_Llamado_Atencion.as_view())), name='Listar_Llamados_Atencion'),
    path('RrHh/llamado_atencion/add', login_required(Crear_Llamado_Atencion.as_view()), name='Crear_Llamado_Atencion'),
    path('RrHh/llamado_atencion/edit/<int:pk>/', login_required(Editar_Llamado_Atencion.as_view()), name='Editar_Llamado_Atencion'),
    # DESCARGOS
    ############################################################################################
    path('RrHh/descargos/list', login_required(Listar_Descargos.as_view()), name='Listar_Descargos'),
    path('RrHh/descargos/add/<int:pk>/', login_required(Crear_Descargos.as_view()), name='Crear_Descargos'),
    path('RrHh/descargos/quiz/<int:pk>/', login_required(Preguntas_Descargos.as_view()), name='Cuestionario_Descargos'),
    path('RrHh/prueba/<int:pk>/', login_required(Prueba_Preguntas_Descargos.as_view()), name='Prueba_Descargos'),
    ############################################################################################
    # CARTAR URLS
    ############################################################################################
    ####################################### URL'S VACACIONES ###################################
    path('RrHh/vacaciones/list', login_required(add_menu_name('VACACIONES')(Listar_Solicitudes_Vacaciones.as_view())), name='Lista_Solicitudes_Vacaciones'),
    path('RrHh/vacaciones/add/', login_required(Vacaciones_Create.as_view()), name='Crear_Solicitud_Vacaciones'),
    path('RrHh/vacaciones/edit/<int:pk>/', login_required(Vacaciones_Edit.as_view()), name='Editar_Solicitud_Vacaciones'),
    path('RrHh/vacaciones/history/<int:pk>/', login_required(Historial_Vacaciones.as_view()), name='Historial_Vacaciones'),
    ############################################################################################

    ############################################################################################
    
    
    # path('RrHh/cartas/renuncia', Crear_Carta_AceptacionRenuncia.as_view(), name='Carta_AceptacionRenuncia'),
    # path('load-modal-content/', load_modal_content, name='load_modal_content'),
    # path('RrHh/pdf', GeneratePDFView.as_view(), name='PDF'),
    path('RrHh/pdf/<int:pk>/', login_required(Contrato_pdf.as_view()), name='PDF_Contrato'),

    ############################################################################################
    path('RrHh/contratos/Select_formato/<int:pk>/', Generar_Carta.as_view(), name='DOC_HV'),
    
    path('RrHh/cartas/list', Listar_Carta.as_view(), name='Listar_Cartas'),
    path('RrHh/cartas/add', Crear_Carta.as_view(), name='Crear_Cartas'),
    # path('RrHh/cartas', Carta_View.as_view(), name='Crear_Cartas'),
    
    path('RrHh/carta_aceptacion_renuncia', Carta_Aceptación_Renuncia_Voluntaria.as_view(), name='Carta_AceptacionRenuncia'),
    path('RrHh/certificado_laboral', Certificado_Laboral.as_view(), name='Certificado_Laboral'),
    path('RrHh/contratos/contrato_aprendizaje', Contrato_Aprendizaje.as_view(), name='Contrato_Aprendizaje'),
    
    
    
    
    # path('userlist/', Listar_Usuario.as_view(), name='Lista_Usuarios'),
    # path('useradd', Crear_Usuario.as_view(), name='Crear_Usuario'),
    # path('useredit/<int:pk>/', Editar_Usuario.as_view(), name= 'Editar_Usuario')

]

