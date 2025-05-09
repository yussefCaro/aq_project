from django.db import models
from decimal import Decimal
from solicitudes.models import Solicitud, Cliente

# Días de auditoría por nivel del CEA
DIAS_AUDITORIA = {
    "Nivel 1": {"etapa_1": 0.5, "etapa_2": 1},
    "Nivel 2": {"etapa_1": 0.5, "etapa_2": 1.5},
    "Nivel 3": {"etapa_1": 0.5, "etapa_2": 2},
    "Nivel 3 con Formación de Instructores": {"etapa_1": 0.5, "etapa_2": 2.5},
}

class Cotizacion(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name="cotizaciones")
    numero_servicio = models.CharField(max_length=100, unique=True)
    fecha_cotizacion = models.DateField(null=True, blank=True)
    tipo_servicio = models.ManyToManyField("TipoServicio")

    dias_auditoria_etapa_1 = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    dias_auditoria_etapa_2 = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    precio_neto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor sin IVA")
    precio_iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), help_text="IVA (19%)")
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), help_text="Total con IVA")

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Rechazada', 'Rechazada'),
        ('Programada', 'Programada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def save(self, *args, **kwargs):
        """ Calcula automáticamente el precio con IVA antes de guardar """
        self.precio_iva = self.precio_neto * Decimal("0.19")
        self.precio_total = self.precio_neto * Decimal("1.19")  # Multiplicación directa
        super().save(*args, **kwargs)

    def __str__(self):
        cliente_nombre = self.solicitud.cliente.nombre_establecimiento if self.solicitud and self.solicitud.cliente else "Sin Cliente"
        return f"Cotización {self.numero_servicio} - {cliente_nombre}"


class TipoServicio(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
