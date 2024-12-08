# Generated by Django 5.1.2 on 2024-11-25 11:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MacroProcesos', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='cargo_macroprocesos',
            old_name='seccion_FK',
            new_name='seccion',
        ),
        migrations.RemoveField(
            model_name='seccion',
            name='proceso_FK',
        ),
        migrations.CreateModel(
            name='Subprocesos',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('IdSubProceso', models.AutoField(primary_key=True, serialize=False)),
                ('SubProceso', models.CharField(blank=True, max_length=100, null=True)),
                ('Observacion', models.CharField(blank=True, max_length=1000)),
                ('dueno', models.ManyToManyField(blank=True, related_name='dueno_subproceso', to='MacroProcesos.cargo_macroprocesos')),
                ('gestorriesgo', models.ManyToManyField(blank=True, related_name='gestor_subproceso', to='MacroProcesos.cargo_macroprocesos')),
                ('proceso_FK', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subproceso', to='MacroProcesos.proceso')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SubProceso',
                'verbose_name_plural': 'SubProcesos',
            },
        ),
        migrations.AddField(
            model_name='cargo_macroprocesos',
            name='subproceso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cargo', to='MacroProcesos.subprocesos'),
        ),
    ]
