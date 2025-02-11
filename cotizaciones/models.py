from django.db import models
from decimal import Decimal
from solicitudes.models import Solicitud  # Importamos la relación con Solicitud
from solicitudes.models import Cliente


# Tipos de servicio permitidos
TIPO_SERVICIO_CHOICES = [
    ("Otorgamiento Inicial", "Otorgamiento Inicial"),
    ("Seguimiento", "Seguimiento"),
    ("Renovación de la Certificación", "Renovación de la Certificación"),
    ("Vigilancia Ordinaria", "Vigilancia Ordinaria"),
    ("Vigilancia Extraordinaria", "Vigilancia Extraordinaria"),
    ("Ampliación de Alcance", "Ampliación de Alcance"),
    ("Reducción de Alcance", "Reducción de Alcance"),
]

# Días de auditoría por nivel del CEA
DIAS_AUDITORIA = {
    "Nivel 1": {"etapa_1": 0.5, "etapa_2": 1},
    "Nivel 2": {"etapa_1": 0.5, "etapa_2": 1.5},
    "Nivel 3": {"etapa_1": 0.5, "etapa_2": 2},
    "Nivel 3 con Formación de Instructores": {"etapa_1": 0.5, "etapa_2": 2.5},
}

class Cotizacion(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    numero_servicio = models.CharField(max_length=10, unique=True, help_text="Formato: XXXX-X")
    fecha_cotizacion = models.DateField(auto_now_add=True)
    tipo_servicio = models.ManyToManyField("TipoServicio", blank=False)

    dias_auditoria_etapa_1 = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    dias_auditoria_etapa_2 = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    precio_neto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor sin IVA")
    precio_iva = models.DecimalField(max_digits=10, decimal_places=2, help_text="IVA (19%)", default=Decimal("0.00"))
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total con IVA", default=Decimal("0.00"))

    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada')],
        default='Pendiente'
    )

    def save(self, *args, **kwargs):
        """ Calcula el IVA (19%) y el precio total antes de guardar """
        self.precio_iva = self.precio_neto * Decimal("0.19")  # Convertimos 0.19 a Decimal
        self.precio_total = self.precio_neto + self.precio_iva
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cotización {self.numero_servicio} - {self.solicitud.cliente.nombre_establecimiento}"


# Modelo para los tipos de servicio
class TipoServicio(models.Model):
    nombre = models.CharField(max_length=50, choices=TIPO_SERVICIO_CHOICES, unique=True)

    def __str__(self):
        return self.nombre


class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Cotizada', 'Cotizada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="solicitudes_cotizaciones")  # Relación con Cliente
    nit = models.CharField(max_length=20, null=True, blank=True, help_text="Número de NIT del cliente")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Solicitud {self.id} - {self.cliente.nombre_establecimiento}"


