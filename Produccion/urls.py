from django.urls import path
from Produccion.views.formicaViews import *
from Produccion.views.medidasView import *
from Produccion.views.grupoFormicaView import *
from Produccion.views.PrecioSuperficieView import *
from django.contrib.auth.decorators import login_required
from ROMIL_BETA1.urls import add_menu_name
app_name = 'Produccion'

urlpatterns = [

    path('Formica/', login_required(add_menu_name('FORMICA')(Listar_Formicas.as_view())), name='Listar_Formica'),
    path('Formica/edit/<int:pk>/', login_required(Editar_Formica.as_view()), name='Editar_Formica'),
    path('Formica/add/', login_required(Crear_FormicaView.as_view()), name='Crear_Formica'),
    path('Formica/delete/<int:pk>/', login_required(Borrar_Formica.as_view()), name='Borrar_Formica'),

    path('Medidas/', login_required(add_menu_name('MEDIDAS')(Listar_Medidas.as_view())), name='Listar_Medidas'),
    path('Medidas/edit/<int:pk>/', login_required(Editar_Medida.as_view()), name='Editar_Medida'),
    path('Medidas/add', login_required(Crear_Medida.as_view()), name='Crear_Medida'),
    path('Medidas/delete/<int:pk>/', login_required(Borrar_Medida.as_view()), name='Borrar_Medida'),

    path('GrupoFormica/', login_required(add_menu_name('GRUPO FORMICA')(Listar_Grupos_Formicas.as_view())), name='Listar_Grupos_Formicas'),
    path('GrupoFormica/edit/<int:pk>/', login_required(Editar_GrupoFormica.as_view()), name='Editar_Grupos_Formicas'),
    path('GrupoFormica/add', login_required(Crear_GrupoFormica.as_view()), name='Crear_Grupos_Formicas'),
    path('GrupoFormica/delete/<int:pk>/', login_required(Borrar_GrupoFormica.as_view()), name='Borrar_Grupos_Formicas'),

    path('PrecioSuperficie/', login_required(add_menu_name('PRECIO SUPERFICIE')(Listar_Precios_Superficie.as_view())), name='Listar_Precios_Superficie'),
    path('PrecioSuperficie/edit/<int:pk>/', login_required(Editar_Precio_Superficie.as_view()), name='Editar_Precios_Superficie'),
    path('PrecioSuperficie/add', login_required(Crear_Precio_Superficie.as_view()), name='Crear_Precios_Superficie'),
    path('PrecioSuperficie/delete/<int:pk>/', login_required(Borrar_Precio_Superficie.as_view()), name='Borrar_Precios_Superficie'),

]

