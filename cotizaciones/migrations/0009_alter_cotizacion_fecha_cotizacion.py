# Generated by Django 5.1.5 on 2025-02-14 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0008_alter_cotizacion_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='fecha_cotizacion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
