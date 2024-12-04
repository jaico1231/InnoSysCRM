from django.urls import path

from ventas.views.carteraView import BuscarCarteraView, CuentasPorCobrarListView, ImprimirCarteraView, enviar_estado_cuenta, PDFCarteraView
from ventas.views.cuentaporcobrarVeiw import CxCListView, CxCUpdateView, CxCDeleteView, CxCCreateView
from ventas.mixins import get_paquete_servicios, get_servicios_adicionales, obtener_saldo_pendiente
from ventas.views.recibocajaView import ObtenerSaldoCuentaView, ReciboCajaCreate2View, ReciboCajaCreateView, ReciboCajaDeleteView, ReciboCajaListView, ReciboCajaUpdateView
from ventas.views.ventasViews import ImprimirFacturaView, VentaCreateView, VentaListView, buscar_servicios, ruta_venta_create, guardar_venta, ver_factura
from django.contrib.auth.decorators import login_required
from InnoSysCRM.urls import add_menu_name
app_name='ventas'

urlpatterns = [
    path('venta/list/', login_required(add_menu_name('VENTAS')(VentaListView.as_view())), name='listar-venta'),
    path('venta/add/', login_required(add_menu_name('CREAR VENTA')(VentaCreateView.as_view())), name='crear-venta'),
    path('venta_pdf/<int:pk>/', login_required(ImprimirFacturaView.as_view()), name='print-venta-pdf'), #print-venta-pdf/<int:pk>/',
    path('venta/ver/<int:pk>/', login_required(ver_factura.as_view()), name='ver_factura'),

    path('api/get-paquete-servicios/', login_required(get_paquete_servicios), name='get-paquete-servicios'),
    path('api/get-servicios-adicionales/', login_required(get_servicios_adicionales), name='get-servicios-adicionales'),
    path('ruta-venta-create/', login_required(ruta_venta_create), name='ruta_venta_create'),
    path('buscar-servicios/', login_required(buscar_servicios), name='buscar-servicios'),
    path('guardar-venta/', login_required(guardar_venta), name='guardar-venta'),
    path('api/cuentas-por-cobrar/<int:cuenta_id>/saldo/', login_required(obtener_saldo_pendiente), name='obtener_saldo_pendiente'),

    path('rc/', login_required(add_menu_name('RECIBO DE CAJA')(ReciboCajaListView.as_view())), name='recibo_caja_list'),
    # path('rc/add', login_required(ReciboCajaCreateView.as_view()), name='RC_create'),
    path('rc/add2', login_required(add_menu_name('CREAR RECIBO')(ReciboCajaCreate2View.as_view())), name='RC_create2'),
    path('rc/edit/<int:pk>/', login_required(ReciboCajaUpdateView.as_view()), name='RC_Update'),
    path('rc/del/<int:pk>/', login_required(ReciboCajaDeleteView.as_view()), name='RC_Del'),
    path('obtener-saldo-cuenta/', login_required(ObtenerSaldoCuentaView.as_view()), name='obtener_saldo_cuenta'),

    path('cxc/', login_required(add_menu_name('CUENTAS POR COBRAR')(CxCListView.as_view())), name='cxc_list'),
    path('cxc/add', login_required(add_menu_name('CREAR CUENTA POR COBRAR')(CxCCreateView.as_view())), name='cxc_Create'),
    path('cxc/edit/<int:pk>/', login_required(CxCUpdateView.as_view()), name='cxc_Update'),
    path('cxc/del/<int:pk>/', login_required(CxCDeleteView.as_view()), name='cxc_Del'),

    path('buscar-cartera/', login_required(add_menu_name('CARTERA')(BuscarCarteraView.as_view())), name='buscar_cartera'),
    path('listar-cuentas/', login_required(CuentasPorCobrarListView.as_view()), name='listar_cuentas'),
    path('imprimir-cartera/<int:pk>/', login_required(PDFCarteraView.as_view()), name='imprimir_cartera'),
    path('email-cartera/', login_required(ImprimirCarteraView.as_view()), name='email_cartera'),    
]
