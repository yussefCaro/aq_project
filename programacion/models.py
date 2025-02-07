from django.db import models
from solicitudes.models import Solicitud

class Programacion(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    fecha_programada = models.DateField()
    asignado_a = models.CharField(max_length=255)

    def __str__(self):
        return f"Programación de {self.solicitud}"
