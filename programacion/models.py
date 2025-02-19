from django.db import models

class NivelAuditoriaCEA(models.Model):
    nivel = models.CharField(max_length=200, unique=True)  # Aumentamos la longitud máxima a 200
    dias_etapa1 = models.FloatField(default=0.5)
    dias_etapa2 = models.FloatField(default=1.0)

    def __str__(self):
        return self.nivel

class Auditor(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=30, unique=True)  # Aumentamos la longitud máxima a 30
    cargo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    iaf_md4_confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"

def obtener_nivel_predeterminado():
    try:
        return NivelAuditoriaCEA.objects.first()
    except NivelAuditoriaCEA.DoesNotExist:
        return None

class ProgramacionAuditoria(models.Model):
    cotizacion = models.ForeignKey('cotizaciones.Cotizacion', on_delete=models.CASCADE)
    nivel_auditoria = models.ForeignKey('NivelAuditoriaCEA',  # O el nombre correcto de tu modelo
        on_delete=models.CASCADE,)
        #null=True,  # ¡Permitir NULL temporalmente!
        #blank=True, # Permitir en el formulario
        #default=None)
    fecha_programacion_etapa1 = models.DateField()
    hora_etapa1 = models.TimeField(default='00:00')
    dias_etapa1 = models.FloatField()  # Permitimos que este valor sea modificado
    auditores = models.ManyToManyField('Auditor')
    iaf_md4_confirmado = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=(
        ('Pendiente', 'Pendiente'),
        ('En Curso', 'En Curso'),
        ('Finalizada', 'Finalizada'),
        ('Cancelada', 'Cancelada'),
    ))  # No establecemos un valor predeterminado para el campo "estado"

    def __str__(self):
        return f"Programación {self.id} - Cotización {self.cotizacion.id}"

class FechaEtapa2(models.Model):
    programacion = models.ForeignKey('ProgramacionAuditoria', on_delete=models.CASCADE, related_name='fechas_etapa2')
    fecha = models.DateField()
    hora = models.TimeField()
    dias_auditoria = models.FloatField(default=0.0)  # Añadimos un valor predeterminado de 0.0

    def __str__(self):
        return str(self.fecha)