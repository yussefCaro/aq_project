from django.contrib import admin
from .models import ProgramacionAuditoria, NivelAuditoriaCEA, Auditor

admin.site.register(ProgramacionAuditoria)
admin.site.register(NivelAuditoriaCEA)
admin.site.register(Auditor)
