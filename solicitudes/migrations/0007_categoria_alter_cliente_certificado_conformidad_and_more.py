# Generated by Django 5.1.5 on 2025-02-08 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0006_alter_cliente_cantidad_vehiculos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3')], max_length=10, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='certificado_conformidad',
            field=models.CharField(choices=[('Si', 'Sí'), ('No', 'No aplica')], default='No', max_length=2),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nivel_cea',
            field=models.CharField(choices=[('Nivel 1', 'Nivel 1'), ('Nivel 2', 'Nivel 2'), ('Nivel 3', 'Nivel 3'), ('Nivel 3 con Formación de Instructores', 'Nivel 3 con Formación de Instructores')], max_length=50),
        ),
        migrations.AddField(
            model_name='cliente',
            name='categorias_certificar',
            field=models.ManyToManyField(blank=True, to='solicitudes.categoria'),
        ),
    ]
