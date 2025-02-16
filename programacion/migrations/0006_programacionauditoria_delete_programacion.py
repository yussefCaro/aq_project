# Generated by Django 5.1.5 on 2025-02-16 12:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0010_alter_cotizacion_solicitud_delete_solicitud'),
        ('programacion', '0005_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramacionAuditoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_programacion_etapa1', models.DateField()),
                ('fecha_programacion_etapa2', models.JSONField(default=list)),
                ('hora_etapa1', models.TimeField(blank=True, null=True)),
                ('hora_etapa2', models.TimeField(blank=True, null=True)),
                ('iaf_md4_confirmado', models.BooleanField(default=False)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Programada', 'Programada'), ('Finalizada', 'Finalizada')], default='Pendiente', max_length=20)),
                ('auditores', models.ManyToManyField(related_name='programaciones', to=settings.AUTH_USER_MODEL)),
                ('cotizacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='programacion', to='cotizaciones.cotizacion')),
            ],
        ),
        migrations.DeleteModel(
            name='Programacion',
        ),
    ]
