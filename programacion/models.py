from django.db import models
from django.contrib.auth.models import User
from cotizaciones.models import Cotizacion  # Importamos Cotizacion desde la app correspondiente

class ProgramacionAuditoria(models.Model):
    cotizacion = models.OneToOneField(Cotizacion, on_delete=models.CASCADE, related_name="programacion")
    auditores = models.ManyToManyField(User, related_name="programaciones")

    fecha_programacion_etapa1 = models.DateField()
    fecha_programacion_etapa2 = models.JSONField(default=list)  # Lista de fechas para etapa 2
    hora_etapa1 = models.TimeField(null=True, blank=True)
    hora_etapa2 = models.TimeField(null=True, blank=True)
    iaf_md4_confirmado = models.BooleanField(default=False)

    ESTADOS_PROGRAMACION = [
        ('Pendiente', 'Pendiente'),
        ('Programada', 'Programada'),
        ('Finalizada', 'Finalizada'),
    ]

    estado = models.CharField(max_length=20, choices=ESTADOS_PROGRAMACION, default='Pendiente')

    def save(self, *args, **kwargs):
        """Sincroniza el estado con la cotización."""
        if self.estado == 'Programada':
            self.cotizacion.estado = 'Programada'
            self.cotizacion.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Programación de {self.cotizacion.numero_servicio} - Estado: {self.estado}'
