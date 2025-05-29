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
                  'firma_representante', 'firma_auditor', 'fecha_inicio', 'fecha_cierre',
                  'aspectos_relevantes',]
        widgets = {
            'aspectos_relevantes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describa aquí los aspectos relevantes observados durante la auditoría',
                'class': 'form-control',
                'representante_legal_nombre': forms.HiddenInput(),
                'representante_legal_cargo': forms.HiddenInput(),
                'fecha_inicio': forms.HiddenInput(),




            }),
        }

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


