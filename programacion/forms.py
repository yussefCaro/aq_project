from django import forms
from .models import ProgramacionAuditoria, Auditor, FechaEtapa2
from django.forms.models import inlineformset_factory  # Importa inlineformset_factory

class ProgramacionAuditoriaForm(forms.ModelForm):
    auditores = forms.ModelChoiceField(
        queryset=Auditor.objects.all(),
        empty_label="Seleccione un auditor",
        required=True
    )
    fecha_programacion_etapa1 = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = ProgramacionAuditoria
        fields = ['cotizacion', 'nivel_auditoria', 'fecha_programacion_etapa1', 'hora_etapa1', 'auditores', 'iaf_md4_confirmado', 'estado']

class FechaEtapa2Form(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = FechaEtapa2
        fields = ['fecha', 'hora']  # dias_auditoria ya no está aquí

FechaEtapa2FormSet = inlineformset_factory(
    ProgramacionAuditoria,  # Modelo principal
    FechaEtapa2,  # Modelo relacionado
    form=FechaEtapa2Form,  # Formulario para el modelo relacionado
    extra=1,  # Número de formularios vacíos adicionales
    max_num=3  # Número máximo de formularios
)