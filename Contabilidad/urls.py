from django.urls import path
from Contabilidad.views.novedades_view import *
from Contabilidad.views.precios_ruta import *
from Contabilidad.views.Horas_Extras_View import *
from django.contrib.auth.decorators import login_required
from ROMIL_BETA1.urls import add_menu_name, print_module
app_name='contabilidad'

urlpatterns = [
    path('procesar-novedades-nomina/', ProcesarNovedadesNominaView.as_view(), name='procesar_novedades_nomina'),
    path('novedades/', login_required(add_menu_name('NOVEDADES')(NovedadNominaListView.as_view())), name='N_N_List'),
    path('novedades/crear/', login_required(NovedadNominaCreateView.as_view()), name='N_N_Create'),
    path('novedades/editar/<int:pk>/', login_required(NovedadNominaUpdateView.as_view()), name='N_N_Update'),
    path('novedades/eliminar/<int:pk>/', login_required(NovedadNominaDeleteView.as_view()), name='N_N_Delete'),
    # Precio de Rutas
    path('precios_ruta/', login_required(add_menu_name('PRECIO DE RUTA')(PreciosRutaView.as_view())), name='P_R_List'),
    path('precios_ruta/crear/', login_required(CreatePreciosRutaView.as_view()), name='P_R_Create'),
    path('precios_ruta/editar/<int:pk>/', login_required(UpdatePreciosRutaView.as_view()), name='P_R_Update'),
    path('precios_ruta/eliminar/<int:pk>/', login_required(DeletePreciosRutaView.as_view()), name='P_R_Delete'),
    # Horas Extras
    path('horas_extras/', login_required(print_module(add_menu_name('HORAS EXTRAS')(HorasExtrasView.as_view()))), name='H_E_List'),
    path('horas_extras/crear/', login_required(CreateHorasExtrasView.as_view()), name='H_E_Create'),
    path('horas_extras/editar/<int:pk>/', login_required(UpdateHorasExtrasView.as_view()), name='H_E_Update'),
    path('horas_extras/eliminar/<int:pk>/', login_required(DeleteHorasExtrasView.as_view()), name='H_E_Delete'),
]
