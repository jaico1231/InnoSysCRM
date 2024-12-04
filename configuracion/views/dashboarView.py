from datetime import datetime
import json
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.db.models import Sum

from ventas.models.ventas import Venta
from ventas.models.ventas import CuentaPorCobrar
from django.db.models import OuterRef, Subquery
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay, TruncYear
from django.utils import timezone
from datetime import timedelta


class DashboardView(TemplateView):
    model = Venta
    template_name = 'administrativo/dashboard.html'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ventas del día actual
        context['venta_dia'] = Venta.objects.filter(fecha=datetime.today()).aggregate(total=Sum('total'))['total'] or 0
        
        # Ventas del mes actual
        today = datetime.today()
        context['venta_mes'] = Venta.objects.filter(fecha__year=today.year, fecha__month=today.month).aggregate(total=Sum('total'))['total'] or 0
        
        # Recibos de caja del mes actual
        context['recibo_mes'] = Venta.objects.filter(fecha__year=today.year, fecha__month=today.month).aggregate(total=Sum('recibos_caja__total'))['total'] or 0
        
        # Cartera pendiente
        context['cartera'] = CuentaPorCobrar.objects.filter(saldo_pendiente__gt=0).aggregate(total=Sum('saldo_pendiente'))['total'] or 0
    

        fecha_hace_siete_dias = timezone.now() - timedelta(days=7)
        # ventas_ultimos_siete_dias = Venta.objects.filter(fecha__gte=fecha_hace_siete_dias).annotate(dia=TruncDay('fecha')).values('dia').annotate(total=Sum('total')).order_by('dia')
        ventas_por_dia = {}
        for i in range(7):
            fecha = (fecha_hace_siete_dias + timedelta(days=i)).date()
            nombre_dia = fecha.strftime('%A')  # Nombre del día en inglés
            ventas_por_dia[nombre_dia] = int(Venta.objects.filter(fecha=fecha).aggregate(total=Sum('total'))['total'] or 0)

        context['ventas_por_dia'] = ventas_por_dia
        
        ventas_por_mes = Venta.objects.filter(fecha__year=timezone.now().year).annotate(mes=TruncMonth('fecha')).values('mes').annotate(total=Sum('total')).order_by('mes')
        # Crear un diccionario para los meses con valor 0 por defecto
        meses = {i: 0 for i in range(1, 13)}  # Diccionario con meses del 1 al 12

        # Llenar el diccionario con los datos de ventas
        for venta in ventas_por_mes:
            mes = venta['mes'].month  # Obtener el mes del objeto de venta
            meses[mes] = int(venta['total'])  # Asignar el total de ventas al mes correspondiente
        
        current_year = datetime.now().year  # Obtener el año actual
        context['ventas_por_mes'] = [(datetime(current_year, mes, 1).strftime('%B'), total) for mes, total in meses.items()]
        # context['ventas_por_mes'] = list(ventas_por_mes)
        
        #  Ventas por año de los últimos 5 años
        fecha_hace_cinco_anos = timezone.now().year - 4
        ventas_por_ano = Venta.objects.filter(fecha__year__gte=fecha_hace_cinco_anos).annotate(ano=TruncYear('fecha')).values('ano').annotate(total=Sum('total')).order_by('ano')
        
        # Crear un diccionario para los años con valor 0 por defecto
        anos = {year: 0 for year in range(fecha_hace_cinco_anos, timezone.now().year + 1)}  # Diccionario con años

        # Llenar el diccionario con los datos de ventas
        for venta in ventas_por_ano:
            ano = venta['ano'].year  # Obtener el año del objeto de venta
            anos[ano] = int(venta['total'])  # Asignar el total de ventas al año correspondiente

        # Convertir el diccionario a una lista de tuplas (año, total)
        context['ventas_por_ano'] = [(ano, total) for ano, total in anos.items()]
        
        
        return context




