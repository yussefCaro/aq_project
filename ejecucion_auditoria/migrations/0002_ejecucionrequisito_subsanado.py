# Generated by Django 5.1.5 on 2025-05-22 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ejecucion_auditoria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ejecucionrequisito',
            name='subsanado',
            field=models.BooleanField(default=False),
        ),
    ]
