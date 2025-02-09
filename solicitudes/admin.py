from django.contrib import admin
from .models import Cliente, Categoria, Solicitud
from .forms import ClienteForm

class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm
    list_display = ("nombre_establecimiento", "nivel_cea", "certificado_conformidad")

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria)
admin.site.register(Solicitud)
