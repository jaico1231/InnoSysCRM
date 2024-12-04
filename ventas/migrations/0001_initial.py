# Generated by Django 5.1.3 on 2024-12-04 03:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuracion', '0001_initial'),
        ('shared', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CuentaPorCobrar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('saldo_pendiente', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('total_cobrado', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuentas_por_cobrar', to='configuracion.medicos')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('fecha', models.DateField()),
                ('numero_factura', models.IntegerField(unique=True)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=60)),
                ('impuestos', models.DecimalField(decimal_places=2, default=0, max_digits=60)),
                ('descuentos', models.DecimalField(decimal_places=2, default=0, max_digits=60)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=60)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('medico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ventas_medico', to='configuracion.medicos')),
                ('metodo_pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pago_venta', to='shared.tipopago')),
                ('tercero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to='shared.terceros')),
                ('tipo_transaccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transacciones_venta', to='shared.tipotransaccion')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReciboCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('fecha', models.DateField()),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('cuenta_por_cobrar', models.ManyToManyField(blank=True, related_name='recibos_caja', to='ventas.cuentaporcobrar')),
                ('metodo_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pago_recibo_caja', to='shared.tipopago')),
                ('tipo_transaccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transacciones_recibo_caja', to='shared.tipotransaccion')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL)),
                ('ventas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recibos_caja', to='ventas.venta')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cuentaporcobrar',
            name='venta',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cuenta_por_cobrar', to='ventas.venta'),
        ),
        migrations.CreateModel(
            name='AnulacionVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL)),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anulaciones', to='ventas.venta')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VentaServicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=50)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('total', models.DecimalField(decimal_places=2, max_digits=50)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.servicios')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL)),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venta_servicios', to='ventas.venta')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]