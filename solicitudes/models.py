from django.db import models

# Create your models here.
class Cliente(models.Model):
    nit = models.CharField(max_length=20, unique=True)  # Nit único
    nombre_propietario = models.CharField(max_length=100)
    nombre_establecimiento = models.CharField(max_length=100)
    representante_legal = models.CharField(max_length=100)
    cedula_ciudadania = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    representante_organismo = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    telefono_fijo = models.CharField(max_length=20, blank=True, null=True)
    telefono_celular = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    nivel_cea = models.CharField(max_length=50)
    cantidad_vehiculos = models.IntegerField()
    cantidad_instructores = models.IntegerField()
    certificado_conformidad = models.CharField(max_length=100, choices=[('si', 'Sí'), ('no', 'No')])
    nombre_ente_certificador = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.nombre_establecimiento









