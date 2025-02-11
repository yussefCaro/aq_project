from django.contrib import admin
from django.utils.html import format_html
from .models import Cotizacion, TipoServicio

class CotizacionAdmin(admin.ModelAdmin):
    list_display = ("numero_servicio", "solicitud", "fecha_cotizacion", "estado", "precio_total_formateado")
    list_filter = ("estado", "fecha_cotizacion")
    search_fields = ("numero_servicio", "solicitud__cliente__nombre_establecimiento")
    filter_horizontal = ("tipo_servicio",)  # Para que el ManyToManyField se vea como lista

    def precio_total_formateado(self, obj):
        """ Formatea el precio total como moneda en el admin """
        return format_html('<b>${:,.2f}</b>', obj.precio_total)

    precio_total_formateado.short_description = "Precio Total"

admin.site.register(Cotizacion, CotizacionAdmin)
admin.site.register(TipoServicio)
