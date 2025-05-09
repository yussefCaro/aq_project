from django.db import models
from django.contrib.auth.models import User

class NivelAuditoriaCEA(models.Model):
    nivel = models.CharField(max_length=200, unique=True)
    dias_etapa1 = models.FloatField(default=0.5)
    dias_etapa2 = models.FloatField(default=1.0)

    def __str__(self):
        return self.nivel



class Auditor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=30, unique=True)
    cargo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    iaf_md4_confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.cargo}"


class ProgramacionAuditoria(models.Model):
    cotizacion = models.ForeignKey('cotizaciones.Cotizacion', on_delete=models.CASCADE)
    nivel_auditoria = models.ForeignKey(NivelAuditoriaCEA, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_programacion_etapa1 = models.DateField(null=True, blank=True)
    hora_etapa1 = models.TimeField(default='00:00')
    auditores = models.ForeignKey(Auditor, on_delete=models.SET_NULL, null=True, blank=True)
    iaf_md4_confirmado = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=(
        ('Pendiente', 'Pendiente'),
        ('En Curso', 'En Curso'),
        ('Finalizada', 'Finalizada'),
        ('Cancelada', 'Cancelada'),
    ), default='Pendiente')  # Valor predeterminado para "estado"

    def __str__(self):
        return f"Programación {self.id} - Cotización {self.cotizacion.id}"

    def save(self, *args, **kwargs):
        # Calcula dias_etapa1 al guardar, usando el nivel_auditoria
        if self.nivel_auditoria:
            self.dias_etapa1 = self.nivel_auditoria.dias_etapa1
        super().save(*args, **kwargs)

class FechaEtapa2(models.Model):
    programacion = models.ForeignKey(ProgramacionAuditoria, on_delete=models.CASCADE, related_name='fechas_etapa2')
    fecha = models.DateField()
    hora = models.TimeField(default='00:00')  # Valor predeterminado para la hora
    # dias_auditoria = models.FloatField(default=0.0)  # Este campo se calcula, no se guarda directamente

    def __str__(self):
        return str(self.fecha)

    def save(self, *args, **kwargs):
        # Calcula dias_auditoria al guardar, usando el nivel_auditoria de la programación
        if self.programacion and self.programacion.nivel_auditoria:
            self.dias_auditoria = self.programacion.nivel_auditoria.dias_etapa2
        super().save(*args, **kwargs)