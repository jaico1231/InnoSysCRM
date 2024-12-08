# Generated by Django 5.1.2 on 2024-11-24 13:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntradaSalida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=7)),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('movimiento', models.CharField(blank=True, choices=[('entregado', 'Entregado'), ('recibido', 'Recibido')], max_length=10, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'EntradaSalida',
                'verbose_name_plural': 'EntradasSalidas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EvaluacionCalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_evaluacion', models.DateTimeField(auto_now_add=True)),
                ('resultado', models.CharField(max_length=100)),
                ('observaciones', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Formica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Formica',
                'verbose_name_plural': 'Formicas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Grupo_Formica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('grupo', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'GrupoFormica',
                'verbose_name_plural': 'GruposFormica',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='MateriaPrima',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad_disponible', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unidad_medida', models.CharField(max_length=20)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'MateriaPrima',
                'verbose_name_plural': 'MateriaPrimas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='MateriaPrimaUsada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_usada', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'MateriaPrimaUsada',
                'verbose_name_plural': 'MateriaPrimaUsadas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Medidas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medida', models.CharField(max_length=100)),
                ('Descripcion', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Medida',
                'verbose_name_plural': 'Medidas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Precio_Superficie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('CFT', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cliente Final Con Transporte')),
                ('CFEF', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cliente Final Entrega en Fabrica')),
                ('PD', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Distribuidor')),
            ],
            options={
                'verbose_name': 'PrecioSuperficie',
                'verbose_name_plural': 'PreciosSuperficies',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProcesoProduccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateTimeField(auto_now_add=True)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'ProcesoProduccion',
                'verbose_name_plural': 'ProcesosProduccion',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductoTerminado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('cantidad_producida', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unidad_medida', models.CharField(max_length=20)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'ProductoTerminado',
                'verbose_name_plural': 'ProductosTerminados',
                'ordering': ['-id'],
            },
        ),
    ]
