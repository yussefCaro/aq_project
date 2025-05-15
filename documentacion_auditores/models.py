# documentacion_auditores/models.py

from django.db import models
from django.contrib.auth.models import User
from programacion.models import ProgramacionAuditoria, NivelAuditoriaCEA


class PlanAuditoria(models.Model):
    programacion = models.OneToOneField(ProgramacionAuditoria, on_delete=models.CASCADE)
    auditor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Auditores"})
    iaf_md4_verificado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)
    fecha_aprobacion = models.DateField()  # Automáticamente, puede ser 2 días antes de etapa 2
    archivo_vehiculos_instructores = models.FileField(upload_to='documentacion/vehiculos_instructores/', null=True, blank=True)
    aprobado_por_cliente = models.BooleanField(default=False)
    fecha_aprobacion_cliente = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Plan Auditoría - {self.programacion.cotizacion.numero_servicio}"

class ActaAuditoria(models.Model):
    plan = models.OneToOneField(PlanAuditoria, on_delete=models.CASCADE, related_name='acta')
    representante_legal_nombre = models.CharField(max_length=255)
    representante_legal_cargo = models.CharField(max_length=100)
    firma_representante = models.ImageField(upload_to='documentacion/firmas/', null=True, blank=True)
    firma_auditor = models.ImageField(upload_to='documentacion/firmas/', null=True, blank=True)
    asistencia = models.TextField(help_text="Lista de asistentes con nombre, cargo y firmas")
    fecha_inicio = models.DateField()
    fecha_cierre = models.DateField()

    def __str__(self):
        return f"Acta Auditoría - {self.plan.programacion.cotizacion.numero_servicio}"



#controlar la asistencia como registros separados
class AsistenteActa(models.Model):
    acta = models.ForeignKey(ActaAuditoria, on_delete=models.CASCADE, related_name='asistentes')
    nombre = models.CharField(max_length=255)
    cargo = models.CharField(max_length=100)
    firma_apertura = models.ImageField(upload_to='documentacion/firmas/', null=True, blank=True)
    firma_cierre = models.ImageField(upload_to='documentacion/firmas/', null=True, blank=True)

# Modelo para la plantilla de actividades por nivel CEA

class ActividadCEA(models.Model):
    nivel = models.ForeignKey(NivelAuditoriaCEA, on_delete=models.CASCADE)
    descripcion = models.TextField("Proceso/Actividad/Requisito por Auditar")
    orden = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nivel} - {self.descripcion[:30]}"


# Modelo para registrar la hora de cada actividad en el plan
class HoraActividadPlan(models.Model):
    plan = models.ForeignKey(PlanAuditoria, on_delete=models.CASCADE, related_name='horas_actividades')
    actividad = models.ForeignKey(ActividadCEA, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.actividad.proceso} - {self.fecha} {self.hora}"

from django.db import models

class VehiculoInstructor(models.Model):
    # Otros campos que quieras (ejemplo: nombre, fecha, etc.)
    archivo_vehiculos_instructores = models.FileField(upload_to='vehiculos_instructores/')

    def __str__(self):
        return f"Archivo: {self.archivo_vehiculos_instructores.name}"




