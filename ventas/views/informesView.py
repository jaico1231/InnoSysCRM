
from ventas.models.ventas import CuentaPorCobrar, ReciboCaja, Venta

def generar_informe_metodo_pago(metodo_pago_id):
    total_ventas = Venta.total_ventas_por_metodo(metodo_pago_id)
    total_pagos = ReciboCaja.total_por_metodo_pago(metodo_pago_id)
    saldo_pendiente = total_ventas - total_pagos

    print(f'Informe para método de pago {metodo_pago_id}:')
    print(f'Total ventas: {total_ventas}')
    print(f'Total pagos recibidos: {total_pagos}')
    print(f'Saldo pendiente: {saldo_pendiente}')

# Ejemplo de uso:
metodo_pago_id = 1
generar_informe_metodo_pago(metodo_pago_id)

from django.db.models import Sum

def obtener_informe_cuentas_pendientes():
    cuentas_pendientes = CuentaPorCobrar.objects.filter(saldo_pendiente__gt=0)
    
    informe = []
    for cuenta in cuentas_pendientes:
        informe.append({
            'numero_factura': cuenta.venta.numero_factura,
            'medico': cuenta.medico,
            'saldo_pendiente': cuenta.saldo_pendiente,
            'total_cobrado': cuenta.total_cobrado,
            'fecha_vencimiento': cuenta.fecha_vencimiento,
        })
    return informe

def obtener_informe_pagos_realizados():
    pagos = ReciboCaja.objects.select_related('cuenta_por_cobrar', 'ventas').all()
    
    informe = []
    for pago in pagos:
        informe.append({
            'numero_factura': pago.ventas.numero_factura,
            'monto_pagado': pago.total,
            'fecha_pago': pago.fecha,
            'metodo_pago': pago.metodo_pago,
        })
    return informe

def verificar_si_cuenta_pagada(venta_id):
    try:
        cuenta = CuentaPorCobrar.objects.get(venta_id=venta_id)
        return cuenta.esta_pagada()
    except CuentaPorCobrar.DoesNotExist:
        return False
