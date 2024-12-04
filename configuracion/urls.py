from django.urls import path
from configuracion.views.dashboarView import DashboardView
from configuracion.views.medicoView import MedicosCreateView, MedicosDeleteView, MedicosListView, MedicosUpdateView
from configuracion.views.relacionespaquetesView import PaqueteServicioCreateView
from configuracion.views.serviciosView import ServiciosListView, ServiciosCreateView, ServiciosUpdateView, ServiciosDeleteView, ToggleServicioEstadoView
from configuracion.views.paquetesView import PaquetesListView, PaquetesCreateView, PaquetesUpdateView, PaquetesDeleteView, TogglePaqueteEstadoView
from django.contrib.auth.decorators import login_required
from InnoSysCRM.urls import add_menu_name
app_name='configuracion'
urlpatterns = [
    path('activeservice/<int:pk>/', login_required(ToggleServicioEstadoView.as_view()), name='estadoservicio'),
    path('activepaquete/<int:pk>/', login_required(TogglePaqueteEstadoView.as_view()), name='estadopaquete'),
    #SERVICIOS    
    path('servicios', login_required(add_menu_name('SERVICIOS')(ServiciosListView.as_view())), name='servicioslist'),
    path('servicios/create', login_required(ServiciosCreateView.as_view()), name='servicioscreate'),
    path('servicios/edit/<int:pk>', login_required(ServiciosUpdateView.as_view()), name='serviciosedit'),
    path('servicios/del/<int:pk>', login_required(ServiciosDeleteView.as_view()), name='serviciosdel'),
    #PAQUETES
    path('paquetes', login_required(add_menu_name('PAQUETES')(PaquetesListView.as_view())), name='paqueteslist'),
    path('paquetes/create', login_required(PaquetesCreateView.as_view()), name='paquetescreate'),
    path('paquetes/edit/<int:pk>', login_required(PaquetesUpdateView.as_view()), name='paquetesedit'),
    path('paquetes/del/<int:pk>', login_required(PaquetesDeleteView.as_view()), name='paquetesdel'),
    #MEDICOS
    path('medicos', login_required(add_menu_name('MEDICOS')(MedicosListView.as_view())), name='medicoslist'),
    path('medicos/create/', login_required(MedicosCreateView.as_view()), name='medicoscreate'),
    path('medicos/update/<int:pk>', login_required(MedicosUpdateView.as_view()), name='medicosupdate'),
    path('medicos/delete/<int:pk>', login_required(MedicosDeleteView.as_view()), name='medicosdelete'),
    #DASHBOARD
    path('dashboard', login_required(add_menu_name('DASHBOARD')(DashboardView.as_view())), name='dashboard'),
    

]
