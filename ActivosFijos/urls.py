from django.urls import path
from django.contrib.auth.decorators import login_required
from ROMIL_BETA1.urls import add_menu_name
from ActivosFijos.views.bitacorasView import *
from ActivosFijos.views.categoriaArticulos_view import *
from ActivosFijos.views.cronogramaView import *
from ActivosFijos.views.indicadores import IndicadoresMantenimientoView
from .views import *

app_name='ACTIVOS'
urlpatterns = [
    path('indicadores/mantenimiento/', login_required(add_menu_name('INDICADORES')(IndicadorCronogramaView.as_view())), name='Indicadores'),
    path('cronograma/', login_required(IndicadoresMantenimientoView.as_view()), name='Cr_Ma'),
    path('cronograma/list/', login_required(add_menu_name('CRONOGRAMA')(Listar_CronogramaView.as_view())), name='Listar_Cronograma'),
    path('cronograma/add', login_required(Crear_CronogramaView.as_view()), name='Crear_Cronograma'),
    path('cronograma/edit/<int:pk>/', login_required(Editar_CronogramaView.as_view()), name='Editar_Cronograma'),
    path('cronograma/delete/<int:pk>/', login_required(Eliminar_CronogramaView.as_view()), name='Eliminar_Cronograma'),

    path('activosfijos/bit/', login_required(add_menu_name('BITACORAS')(Listar_BitacoraView.as_view())), name='Listar_Bit'),
    path('activosfijos/bit/add', login_required(Crear_BitacoraView.as_view()), name='Crear_Bit'),
    path('activosfijos/bit/edit/<int:pk>/', login_required(Editar_BitacoraView.as_view()), name='Editar_Bit'),
    path('activosfijos/bit/delete/<int:pk>/', login_required(Borrar_BitacoraView.as_view()), name='Borrar_Bit'),

    path('activosfijos/presupuesto/', login_required(add_menu_name('PRESUPUESTO')(PresupuestoView.as_view())), name='Listar_PRESUPUESTO'),
    path('activosfijos/presupuesto/add', login_required(Crear_PresupuestoView.as_view()), name='Crear_PRESUPUESTO'),
    path('activosfijos/presupuesto/edit/<int:pk>/', login_required(Editar_PresupuestoView.as_view()), name='Editar_PRESUPUESTO'),
    path('activosfijos/presupuesto/delete/<int:pk>/', login_required(Borrar_PresupuestoView.as_view()), name='Borrar_PRESUPUESTO'),

    path('activosfijos/area_trabajo/', login_required(add_menu_name('AREA DE TRABAJO')(Area_TrabajoView.as_view())), name='Listar_AT'),
    path('activosfijos/area_trabajo/add', login_required(Crear_Area_TrabajoView.as_view()), name='Crear_AT'),
    path('activosfijos/area_trabajo/edit/<int:pk>/', login_required(Editar_Area_TrabajoView.as_view()), name='Editar_AT'),
    path('activosfijos/area_trabajo/delete/<int:pk>/', login_required(Borrar_Area_TrabajoView.as_view()), name='Borrar_AT'),

    path('activosfijos/Grupos/', login_required(add_menu_name('CATEGORIA ARTICULOS')(Listar_Categoria_ArticulosView.as_view())), name='Listar_GRUPO_ART'),
    path('activosfijos/Grupos/add', login_required(Crear_Categoria_ArticulosView.as_view()), name='Crear_GRUPO_ART'),
    path('activosfijos/Grupos/edit/<int:pk>/', login_required(Editar_Categoria_ArticulosView.as_view()), name='Editar_GRUPOART'),
    path('activosfijos/Grupos/delete/<int:pk>/', login_required(Eliminar_Categoria_ArticulosView.as_view()), name='Borrar_GRUPO_ART'),

    path('activosfijos/articulos/', login_required(add_menu_name('ARTICULOS')(Listar_ArticulosView.as_view())), name='Listar_ART'),
    path('activosfijos/articulos/add', login_required(Crear_ArticulosView.as_view()), name='Crear_ART'),
    path('activosfijos/articulos/edit/<int:pk>/', login_required(Editar_ArticulosView.as_view()), name='Editar_ART'),
    path('activosfijos/articulos/delete/<int:pk>/', login_required(Borrar_ArticulosView.as_view()), name='Borrar_ART'),

    path('activosfijos/anexosart/<int:pk>/', login_required(Anexos_ArticulosView.as_view()), name='Anexos_ART'),
    path('activosfijos/anexosart/add', login_required(Crear_Anexos_ArticulosView.as_view()), name='Crear_Anexos_ART'),
    path('activosfijos/anexosart/edit/<int:pk>/', login_required(Editar_Anexos_ArticulosView.as_view()), name='Editar_Anexos_ART'),
    path('activosfijos/anexosart/delete/<int:pk>/', login_required(Borrar_Anexos_ArticulosView.as_view()), name='Borrar_Anexos_ART'),

    path('activosfijos/inventario/', login_required(add_menu_name('INVENTARIO')(InventarioView.as_view())), name='Inventario'),
    path('activosfijos/inventario/movimiento', login_required(RegistrarMovimientoView.as_view()), name='Movimiento'),

    path('activosfijos/ordenservicio/', login_required(add_menu_name('ORDEN DE SERVICIO')(Listar_OrdenesServicioView.as_view())), name='Listar_OS'),
    path('activosfijos/ordenservicio/add', login_required(Crear_OrdenesServicioView.as_view()), name='Crear_OS'),
    path('activosfijos/ordenservicio/detail/<int:pk>/', login_required(Detail_OrdenesServicioView.as_view()), name='Detail_OS'),
    path('activosfijos/ordenservicio/edit/<int:pk>/', login_required(Editar_OrdenesServicioView.as_view()), name='Editar_OS'),
    path('activosfijos/ordenservicio/delete/<int:pk>/', login_required(Borrar_OrdenesServicioView.as_view()), name='Borrar_OS'),

    path('activosfijos/hv-art/', login_required(add_menu_name('HV ARTICULOS')(Listar_Hoja_Vida_ArticulosView.as_view())), name='Listar_HV_ART'),
    path('activosfijos/hv-art/add', login_required(Crear_Hoja_Vida_ArticulosView.as_view()), name='Crear_HV_ART'),
    path('activosfijos/hv-art/edit/<int:pk>/', login_required(Editar_Hoja_Vida_ArticulosView.as_view()), name='Editar_HV_ART'),
    path('activosfijos/hv-art/delete/<int:pk>/', login_required(Borrar_Hoja_Vida_ArticulosView.as_view()), name='Borrar_HV_ART'),

    
    
    # path('activosfijos/', Listar_ActivosFijos.as_view(), name='Listar_AF'),

]