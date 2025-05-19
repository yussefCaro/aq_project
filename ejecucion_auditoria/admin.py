from django.contrib import admin
from .models import RequisitoAuditoria, EjecucionRequisito, NoConformidad

admin.site.register(RequisitoAuditoria)
admin.site.register(EjecucionRequisito)
admin.site.register(NoConformidad)


