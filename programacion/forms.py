from django import forms
from .models import ProgramacionAuditoria, Auditor, FechaEtapa2

class ProgramacionAuditoriaForm(forms.ModelForm):
    auditores = forms.ModelMultipleChoiceField(
        queryset=Auditor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = ProgramacionAuditoria
        fields = ['cotizacion', 'nivel_auditoria', 'fecha_programacion_etapa1', 'hora_etapa1', 'auditores', 'iaf_md4_confirmado', 'estado']

class FechaEtapa2Form(forms.ModelForm):
    class Meta:
        model = FechaEtapa2
        fields = ['fecha', 'hora', 'dias_auditoria']

FechaEtapa2FormSet = forms.modelformset_factory(FechaEtapa2, form=FechaEtapa2Form, extra=3, max_num=3)
