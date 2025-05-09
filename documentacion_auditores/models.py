# documentacion_auditores/models.py

from django.db import models
from django.contrib.auth.models import User
from programacion.models import ProgramacionAuditoria  # Ajusta al nombre real de tu modelo

class PlanAuditoria(models.Model):
    programacion = models.OneToOneField(ProgramacionAuditoria, on_delete=models.CASCADE)
    auditor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Auditores"})
    iaf_md4_verificado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)
    fecha_aprobacion = models.DateField()  # Automáticamente, puede ser 2 días antes de etapa 2
    archivo_vehiculos_instructores = models.FileField(upload_to='documentacion/vehiculos_instructores/', null=True, blank=True)

    def __str__(self):
        return f"Plan Auditoría - {self.programacion.cotizacion.numero_servicio}"

class ActaAuditoria(models.Model):
    programacion = models.OneToOneField(ProgramacionAuditoria, on_delete=models.CASCADE)
    representante_legal_nombre = models.CharField(max_length=255)
    representante_legal_cargo = models.CharField(max_length=100)
    firma_representante = models.ImageField(upload_to='documentacion/firmas/', null=True, blank=True)
    firma_auditor = models.ImageField(upload_to='documentacion/firmas/', null=True, blank=True)
    asistencia = models.TextField(help_text="Lista de asistentes con nombre, cargo y firmas")

    fecha_inicio = models.DateField()
    fecha_cierre = models.DateField()

    def __str__(self):
        return f"Acta Auditoría - {self.programacion.cotizacion.numero_servicio}"


#controlar la asistencia como registros separados
class AsistenteActa(models.Model):
    acta = models.ForeignKey(ActaAuditoria, on_delete=models.CASCADE, related_name='asistentes')
    nombre = models.CharField(max_length=255)
    cargo = models.CharField(max_length=100)
    firma_apertura = models.ImageField(upload_to='documentacion/firmas/', null=True, blank=True)
    firma_cierre = models.ImageField(upload_to='documentacion/firmas/', null=True, blank=True)

