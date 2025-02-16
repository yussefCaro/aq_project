# Generated by Django 5.1.5 on 2025-02-05 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('solicitudes', '0004_solicitud'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_programada', models.DateField()),
                ('asignado_a', models.CharField(max_length=255)),
                ('solicitud', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.solicitud')),
            ],
        ),
    ]
