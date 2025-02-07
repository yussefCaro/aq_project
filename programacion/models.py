from django.db import models
from solicitudes.models import Solicitud  # Importamos el modelo Solicitud
from django.contrib.auth.models import User  # Importamos User para asignar auditores

class Programacion(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    fecha_auditoria = models.DateField(null=True, blank=True)
    auditor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="auditorias")
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada'), ('Programada', 'Programada')],
        default='Pendiente'
    )

    def __str__(self):
        return f"Auditoría para {self.solicitud.cliente.nombre_establecimiento} - {self.fecha_auditoria}"

