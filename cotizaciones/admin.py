from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import SafeString
from decimal import Decimal

from .models import Cotizacion, TipoServicio

class CotizacionAdmin(admin.ModelAdmin):
    list_display = ("numero_servicio", "solicitud", "fecha_cotizacion", "estado", "precio_total_formateado")
    list_filter = ("estado", "fecha_cotizacion")
    search_fields = ("numero_servicio", "solicitud__cliente__nombre_establecimiento")
    filter_horizontal = ("tipo_servicio",)  # Para que el ManyToManyField se vea como lista



    def precio_total_formateado(self, obj):
        """ Formatea el precio total como moneda en el admin """
        if obj.precio_total is None:
            return "-"

        try:
            # Asegurar que el valor sea Decimal o float antes de formatear
            precio = Decimal(obj.precio_total)  # Convertir a Decimal directamente
        except (ValueError, TypeError):
            return obj.precio_total  # Devolver sin formato si no es convertible

        # Retornar una cadena sin formato_html para evitar el error
        return "${:,.2f}".format(float(precio))

    precio_total_formateado.short_description = "Precio Total"


admin.site.register(Cotizacion, CotizacionAdmin)
admin.site.register(TipoServicio)
