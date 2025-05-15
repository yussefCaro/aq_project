from django import forms
from .models import PlanAuditoria, ActaAuditoria, AsistenteActa

class PlanAuditoriaForm(forms.ModelForm):
    class Meta:
        model = PlanAuditoria
        fields = ['iaf_md4_verificado', 'observaciones', 'archivo_vehiculos_instructores']

class ActaAuditoriaForm(forms.ModelForm):
    class Meta:
        model = ActaAuditoria
        fields = ['representante_legal_nombre', 'representante_legal_cargo',
                  'firma_representante', 'firma_auditor', 'fecha_inicio', 'fecha_cierre']

class AsistenteActaForm(forms.ModelForm):
    class Meta:
        model = AsistenteActa
        fields = ['nombre', 'cargo']
        exclude = ['firma_apertura', 'firma_cierre']


from django.forms import modelformset_factory
from .models import HoraActividadPlan

HoraActividadPlanFormSet = modelformset_factory(
    HoraActividadPlan,
    fields=('fecha', 'hora'),
    extra=0
)


