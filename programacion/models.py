from django.db import models
from solicitudes.models import Solicitud  # Importamos el modelo Solicitud
from django.contrib.auth.models import User  # Importamos User para asignar auditores
import json

class Programacion(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)

    # Etapa 1
    fecha_etapa_1 = models.DateField(null=True, blank=True)
    hora_etapa_1 = models.TimeField(null=True, blank=True)
    dias_auditoria_etapa_1 = models.DecimalField(max_digits=3, decimal_places=1, default=0.5)

    # Etapa 2
    fecha_etapa_2 = models.JSONField(null=True, blank=True)  # Almacena hasta 3 fechas en formato JSON
    hora_etapa_2 = models.TimeField(null=True, blank=True)
    dias_auditoria_etapa_2 = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    auditor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="auditorias")
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Aprobada', 'Aprobada'),
            ('Rechazada', 'Rechazada'),
            ('Programada', 'Programada'),
        ],
        default='Pendiente'
    )

    def calcular_dias_auditoria(self):
        """Retorna los días de auditoría de la etapa 2 según el nivel del CEA."""
        niveles = {
            "Nivel 1": 1,
            "Nivel 2": 1.5,
            "Nivel 3": 2,
            "Nivel 3 con Formación de Instructores": 2.5,
        }
        return niveles.get(self.solicitud.cliente.nivel_cea, 1)  # Retorna el valor según el nivel del CEA

    def save(self, *args, **kwargs):
        """Asigna automáticamente los días de auditoría en la etapa 2 según el nivel del CEA."""
        if not self.dias_auditoria_etapa_2:
            self.dias_auditoria_etapa_2 = self.calcular_dias_auditoria()

        # Convertir lista de fechas en JSON si es necesario
        if isinstance(self.fecha_etapa_2, list):
            self.fecha_etapa_2 = json.dumps(self.fecha_etapa_2)

        super().save(*args, **kwargs)

    def get_fecha_etapa_2(self):
        """Devuelve las fechas de la etapa 2 como una lista si es posible."""
        if self.fecha_etapa_2:
            return json.loads(self.fecha_etapa_2)
        return []

    def __str__(self):
        return f"Auditoría para {self.solicitud.cliente.nombre_establecimiento} - {self.fecha_etapa_1} / {self.fecha_etapa_2}"
