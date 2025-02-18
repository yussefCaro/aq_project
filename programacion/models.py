from django.db import models

class NivelAuditoriaCEA(models.Model):
    nivel = models.CharField(max_length=100, unique=True)
    dias_etapa1 = models.FloatField(default=0.5)  # Etapa 1 siempre es 0.5 días
    dias_etapa2 = models.FloatField()

    def __str__(self):
        return self.nivel

class Auditor(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    iaf_md4_confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"

class ProgramacionAuditoria(models.Model):
    cotizacion = models.ForeignKey('cotizaciones.Cotizacion', on_delete=models.CASCADE)
    nivel_auditoria = models.ForeignKey(NivelAuditoriaCEA, on_delete=models.CASCADE)
    fecha_programacion_etapa1 = models.DateField()
    hora_etapa1 = models.TimeField()
    fecha_programacion_etapa2 = models.JSONField(default=list)  # Admite hasta 3 fechas
    hora_etapa2 = models.TimeField()
    auditores = models.ManyToManyField(Auditor)  # Relación con múltiples auditores
    iaf_md4_confirmado = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, default="Pendiente")

    def save(self, *args, **kwargs):
        # Restricción de máximo 3 fechas en etapa 2
        if len(self.fecha_programacion_etapa2) > 3:
            raise ValueError("No puedes agregar más de 3 fechas para la etapa 2.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Programación {self.id} - Cotización {self.cotizacion.id}"
