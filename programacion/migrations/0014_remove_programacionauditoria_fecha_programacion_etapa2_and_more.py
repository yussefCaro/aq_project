from django.db import migrations, models
import django.db.models.deletion

def crear_niveles_iniciales(apps, schema_editor):
    NivelAuditoriaCEA = apps.get_model('programacion', 'NivelAuditoriaCEA')
    niveles_a_crear = [
        {"nivel": "Nivel 1", "dias_etapa1": 0.5, "dias_etapa2": 1.0},
        {"nivel": "Nivel 2", "dias_etapa1": 1.0, "dias_etapa2": 1.5},
        {"nivel": "Nivel 3", "dias_etapa1": 0.5, "dias_etapa2": 2.0},
        {"nivel": "Nivel 3 con Formación de ...", "dias_etapa1": 0.5, "dias_etapa2": 2.5},
        {"nivel": "Nivel 1 Nuevo", "dias_etapa1": 0.5, "dias_etapa2": 1.0},
    ]

    for nivel_data in niveles_a_crear:
        NivelAuditoriaCEA.objects.get_or_create(nivel=nivel_data['nivel'], defaults=nivel_data)

class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0012_remove_cotizacion_nivel_cea'),
        ('programacion', '0013_remove_programacionauditoria_nivel_auditoria_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programacionauditoria',
            name='fecha_programacion_etapa2',
        ),
        migrations.RemoveField(
            model_name='programacionauditoria',
            name='hora_etapa2',
        ),
        migrations.AddField(
            model_name='programacionauditoria',
            name='dias_etapa1',
            field=models.FloatField(default=0.5),
        ),
        migrations.AddField(
            model_name='programacionauditoria',
            name='nivel_auditoria',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='programacion.nivelauditoriacea'),  # default=None temporalmente
        ),
        migrations.RunPython(crear_niveles_iniciales),  # ¡Ahora va después de AddField!
        migrations.AlterField(  # Asigna el valor correcto a nivel_auditoria después de crear los niveles
            model_name='programacionauditoria',
            name='nivel_auditoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='programacion.nivelauditoriacea'),  # Reemplaza 1 con el ID del primer NivelAuditoriaCEA
        ),
        migrations.AlterField(
            model_name='auditor',
            name='cargo',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='nivelauditoriacea',
            name='dias_etapa1',
            field=models.FloatField(default=0.5),
        ),
        migrations.AlterField(
            model_name='nivelauditoriacea',
            name='dias_etapa2',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='nivelauditoriacea',
            name='nivel',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='programacionauditoria',
            name='auditores',
            field=models.ManyToManyField(to='programacion.auditor'),
        ),
        migrations.AlterField(
            model_name='programacionauditoria',
            name='cotizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizaciones.cotizacion'),
        ),
        migrations.AlterField(
            model_name='programacionauditoria',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('En Curso', 'En Curso'), ('Finalizada', 'Finalizada'), ('Cancelada', 'Cancelada')], default='Pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='programacionauditoria',
            name='hora_etapa1',
            field=models.TimeField(default='00:00'),
        ),
        migrations.CreateModel(
            name='FechaEtapa2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('dias_auditoria', models.FloatField()),
                ('programacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fechas_etapa2', to='programacion.programacionauditoria')),
            ],
        ),
    ]