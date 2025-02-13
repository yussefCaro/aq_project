# Generated by Django 5.1.5 on 2025-02-07 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programacion', '0002_remove_programacion_asignado_a_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programacion',
            old_name='fecha_auditoria',
            new_name='fecha_etapa_1',
        ),
        migrations.AddField(
            model_name='programacion',
            name='dias_auditoria_etapa_1',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=3),
        ),
        migrations.AddField(
            model_name='programacion',
            name='dias_auditoria_etapa_2',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='programacion',
            name='fecha_etapa_2',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='programacion',
            name='hora_etapa_1',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='programacion',
            name='hora_etapa_2',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
