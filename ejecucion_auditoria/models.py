from django.db import models
from documentacion_auditores.models import ActaAuditoria

class RequisitoAuditoria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    checkpoint_iaf_md4 = models.CharField(max_length=100, blank=True)
    # Puedes agregar campos como categoria, orden, etc. si lo necesitas

    def __str__(self):
        return self.nombre

class EjecucionRequisito(models.Model):
    acta = models.ForeignKey(ActaAuditoria, on_delete=models.CASCADE, related_name='ejecuciones')
    requisito = models.ForeignKey(RequisitoAuditoria, on_delete=models.CASCADE)
    cumple = models.BooleanField(default=False, blank=True)
    no_cumple = models.BooleanField(default=False, blank=True)
    no_aplica = models.BooleanField(default=False, blank=True)
    aspecto_mejora = models.BooleanField(default=False, blank=True)
    concepto_mejora = models.TextField(blank=True)
    concepto_no_conformidad = models.TextField(blank=True)
    evidencia = models.CharField(
        max_length=100,
        blank=True,
        choices=[
            ("documental", "Evidencia Documental"),
            ("fotografica", "Evidencia Fotográfica"),
            ("audiovisual", "Evidencia Audiovisual"),
            ("documental_fotografica", "Evidencia Documental y Fotográfica"),
            ("documental_audiovisual", "Evidencia Documental y Audiovisual"),
            ("fotografica_audiovisual", "Evidencia Fotográfica y Audiovisual"),
            ("documental_fotografica_audiovisual", "Evidencia Documental, Fotográfica y Audiovisual"),
        ]
    )
    concepto_evidencia = models.TextField(blank=True)
    imagen1 = models.ImageField(upload_to='evidencias/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='evidencias/', blank=True, null=True)
    subsanado = models.BooleanField(default=False, blank=True)
    como_se_subsano = models.TextField(blank=True, verbose_name="¿Cómo se subsanó la no conformidad?")
    # Puedes agregar campos como fecha de registro, usuario, etc.

    def __str__(self):
        return f"{self.acta} - {self.requisito}"

class NoConformidad(models.Model):
    ejecucion = models.OneToOneField(EjecucionRequisito, on_delete=models.CASCADE)
    subsanado = models.BooleanField(default=False, blank=True)
    comentario_subsanacion = models.TextField(blank=True)
    fecha_subsanacion = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"No conformidad en: {self.ejecucion}"
