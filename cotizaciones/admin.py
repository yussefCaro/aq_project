from django.contrib import admin
from .models import Cotizacion, TipoServicio

class CotizacionAdmin(admin.ModelAdmin):
    list_display = ("numero_servicio", "solicitud", "fecha_cotizacion", "estado", "precio_total")
    list_filter = ("estado", "fecha_cotizacion")
    search_fields = ("numero_servicio", "solicitud__cliente__nombre_establecimiento")
    filter_horizontal = ("tipo_servicio",)  # Para que el ManyToManyField se vea como lista

admin.site.register(Cotizacion, CotizacionAdmin)
admin.site.register(TipoServicio)
