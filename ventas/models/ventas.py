
from datetime import date, timedelta
from django.db import models
from configuracion.models.servicios import Medicos, Servicios
from shared.models.baseModel import BaseModel
from shared.models.terceros import Terceros
from shared.models.tipo_pago import TipoPago, TipoTransaccion
from django.db.models import Sum

class Venta(BaseModel):
    tercero = models.ForeignKey(Terceros, on_delete=models.CASCADE, related_name='ventas')
    medico = models.ForeignKey(Medicos, on_delete=models.CASCADE, related_name='ventas_medico', null=True, blank=True)
    fecha = models.DateField()
    numero_factura = models.IntegerField(unique=True)
    metodo_pago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, related_name='pago_venta', null=True, blank=True)
    tipo_transaccion = models.ForeignKey(TipoTransaccion, on_delete=models.CASCADE, related_name='transacciones_venta', null=True, blank=True)
    subtotal = models.DecimalField(max_digits=60, decimal_places=2, default=0)  # Total sin impuestos
    impuestos = models.DecimalField(max_digits=60, decimal_places=2, default=0)  # IVA
    descuentos = models.DecimalField(max_digits=60, decimal_places=2, default=0)  # Descuentos generales
    total = models.DecimalField(max_digits=60, decimal_places=2, default=0)  # Total final con impuestos
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Venta a {self.id}'

    def pagos_recibidos(self):
        """
        Calcula el total de pagos recibidos por esta venta.
        """
        return self.recibos_caja.aggregate(total_pagado=Sum('total'))['total_pagado'] or 0

    def saldo_pendiente(self):
        """
        Calcula el saldo pendiente en esta venta.
        """
        return self.total - self.pagos_recibidos()

    def es_credito(self):
        """
        Verifica si esta venta fue a crédito o no.
        """
        return self.metodo_pago and self.metodo_pago.nombre.lower() == 'credito'

class VentaServicios(BaseModel):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='venta_servicios')
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=50, decimal_places=2)
    descuento = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=50, decimal_places=2)

    def __str__(self):
        return f'{self.servicio} en la venta de {self.venta}'

class AnulacionVenta(BaseModel):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='anulaciones')
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Anulacion de {self.venta}'

class CuentaPorCobrar(BaseModel):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='cuenta_por_cobrar')
    medico = models.ForeignKey(Medicos, on_delete=models.CASCADE, related_name='cuentas_por_cobrar')
    fecha_vencimiento = models.DateField(null=True, blank=True)  # Fecha límite para el pago de la cuenta por cobrar
    saldo_pendiente = models.DecimalField(max_digits=50, decimal_places=2, default=0)  # Monto que queda por cobrar
    total_cobrado = models.DecimalField(max_digits=50, decimal_places=2, default=0)  # Total ya cobrado de la cuenta
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'CC-Factura {self.venta.numero_factura} por {self.medico}'

    def registrar_pago(self, recibo_caja, monto_pagado):
        """
        Registra un pago parcial o total en la cuenta por cobrar y lo relaciona con un recibo de caja.
        """
        self.total_cobrado += monto_pagado
        self.saldo_pendiente = max(0, self.saldo_pendiente - monto_pagado)  # Asegurar que no quede negativo
        self.save()

        # Relacionar la cuenta por cobrar con el recibo de caja usando `add()`
        recibo_caja.cuenta_por_cobrar.add(self)  # Relaciona la cuenta con el recibo
        recibo_caja.total += monto_pagado  # Actualiza el total en el recibo con el monto pagado
        recibo_caja.save()

    def esta_pagada(self):
        """
        Verifica si la cuenta por cobrar ha sido pagada en su totalidad.
        """
        return self.saldo_pendiente <= 0
    
class ReciboCaja(BaseModel):
    ventas = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='recibos_caja', null=True, blank=True)
    cuenta_por_cobrar = models.ManyToManyField(CuentaPorCobrar, related_name='recibos_caja', blank=True)  # Cambiado a ManyToManyField
    fecha = models.DateField()
    metodo_pago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, related_name='pago_recibo_caja')
    tipo_transaccion = models.ForeignKey(TipoTransaccion, on_delete=models.CASCADE, related_name='transacciones_recibo_caja', null=True, blank=True)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Recibo N° {self.id}'
