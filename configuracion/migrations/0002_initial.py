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
        migrations.AddField(
            model_name='medico_paquetes',
            name='user_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medico_paquetes',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicos',
            name='tercero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terceros', to='shared.terceros'),
        ),
        migrations.AddField(
            model_name='medicos',
            name='user_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicos',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medico_paquetes',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicos_paquetes', to='configuracion.medicos'),
        ),
        migrations.AddField(
            model_name='paquetes',
            name='user_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paquetes',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medico_paquetes',
            name='paquete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paquetes_medicos', to='configuracion.paquetes'),
        ),
        migrations.AddField(
            model_name='paquetesservicios',
            name='paquete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paquetes_servicios', to='configuracion.paquetes'),
        ),
        migrations.AddField(
            model_name='paquetesservicios',
            name='user_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paquetesservicios',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servicios',
            name='user_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servicios',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paquetesservicios',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios_paquetes', to='configuracion.servicios'),
        ),
        migrations.AddField(
            model_name='paquetes',
            name='servicios',
            field=models.ManyToManyField(related_name='paquetes', through='configuracion.PaquetesServicios', to='configuracion.servicios'),
        ),
        migrations.AlterUniqueTogether(
            name='medico_paquetes',
            unique_together={('medico', 'paquete')},
        ),
        migrations.AlterUniqueTogether(
            name='paquetesservicios',
            unique_together={('paquete', 'servicio')},
        ),
    ]