from django.urls import path
from Comercial.views.cotizacionesView import CrearCotizacionView, EditarCotizacionView
from ROMIL_BETA1.urls import add_menu_name
from django.contrib.auth.decorators import login_required
app_name = 'comercial'

urlpatterns = [
    path('cotizaciones/', login_required(add_menu_name('COTIZACIONES')(CrearCotizacionView.as_view())), name='cot_create'),
    path('cotizaciones/editar/<int:pk>/',login_required( EditarCotizacionView.as_view()), name='cot_edit'),
    # Otras URLs
]