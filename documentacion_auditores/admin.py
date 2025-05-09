from django.contrib import admin
from .models import PlanAuditoria, ActaAuditoria, AsistenteActa

admin.site.register(PlanAuditoria)
admin.site.register(ActaAuditoria)
admin.site.register(AsistenteActa)

