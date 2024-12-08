from django.urls import path
from MacroProcesos.views.macro_procesos_view import Listar_MacroProcesos, Crear_MacroProcesos, Editar_MacroProcesos, Eliminar_MacroProcesos
from MacroProcesos.views.procesos_view import Listar_Procesos, Crear_Procesos, Editar_Procesos, Eliminar_Procesos
from MacroProcesos.views.subprocesos_view import Listar_Subprocesos, Crear_Subprocesos, Editar_Subprocesos, Eliminar_Subprocesos
from MacroProcesos.views.seccion_view import Listar_Seccion, Crear_Seccion, Editar_Seccion, Eliminar_Seccion
from MacroProcesos.views.cargos_view import Listar_Cargos, Crear_Cargos, Editar_Cargos, Eliminar_Cargos
from django.contrib.auth.decorators import login_required
from ROMIL_BETA1.urls import add_menu_name

app_name='macroprocesos'
urlpatterns = [
    path('Lista_M_P/', login_required(add_menu_name('MACRO PROCESOS')(Listar_MacroProcesos.as_view())), name='Listar_MacroProcesos'),
    path('Crear_M_P/', login_required(Crear_MacroProcesos.as_view()), name='Crear_MacroProcesos'),
    path('Editar_M_P/<pk>', login_required(Editar_MacroProcesos.as_view()), name='Editar_MacroProcesos'),
    path('Eliminar_M_P/<pk>', login_required(Eliminar_MacroProcesos.as_view()), name='Eliminar_MacroProcesos'),
    ############################################################################################################
 
    path('procesos/', login_required(add_menu_name('PROCESOS')(Listar_Procesos.as_view())), name='Listar_Procesos'),
    path('add_procesos/', login_required(Crear_Procesos.as_view()), name='Crear_Procesos'),
    path('edit_procesos/<int:pk>', login_required(Editar_Procesos.as_view()), name='Editar_Procesos'),
    path('delete_procesos/<int:pk>', login_required(Eliminar_Procesos.as_view()), name='Eliminar_Procesos'),
    ############################################################################################################

    path('subprocesos/', login_required(add_menu_name('SUBPROCESOS')(Listar_Subprocesos.as_view())), name='Listar_Subprocesos'),
    path('add_subprocesos/', login_required(Crear_Subprocesos.as_view()), name='Crear_Subprocesos'),
    path('edit_subprocesos/<int:pk>', login_required(Editar_Subprocesos.as_view()), name='Editar_Subprocesos'),
    path('delete_subprocesos/<int:pk>', login_required(Eliminar_Subprocesos.as_view()), name='Eliminar_Subprocesos'),
    ############################################################################################################
    
    path('seccion/', login_required(add_menu_name('SECCION')(Listar_Seccion.as_view())), name='Listar_Seccion'),
    path('add_seccion/', login_required(Crear_Seccion.as_view()), name='Crear_Seccion'),
    path('edit_seccion/<pk>', login_required(Editar_Seccion.as_view()), name='Editar_Seccion'),
    path('delete_seccion/<pk>', login_required(Eliminar_Seccion.as_view()), name='Eliminar_Seccion'),
    ############################################################################################################
 
    path('cargo/', login_required(add_menu_name('CARGOS')(Listar_Cargos.as_view())), name='Listar_Cargo'),
    path('add_cargo/', login_required(Crear_Cargos.as_view()), name='Crear_Cargo'),
    path('edit_cargo/<pk>', login_required(Editar_Cargos.as_view()), name='Editar_Cargo'),
    path('delete_cargo/<pk>', login_required(Eliminar_Cargos.as_view()), name='Eliminar_Cargo'),

]