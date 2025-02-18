from django import forms
from .models import ProgramacionAuditoria, Auditor

class ProgramacionAuditoriaForm(forms.ModelForm):
    fecha_programacion_etapa2 = forms.CharField(
        required=False,
        help_text="Ingrese hasta 3 fechas separadas por comas"
    )
    auditores = forms.ModelMultipleChoiceField(
        queryset=Auditor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = ProgramacionAuditoria
        fields = [
            'cotizacion', 'nivel_auditoria', 'fecha_programacion_etapa1', 'hora_etapa1',
            'fecha_programacion_etapa2', 'hora_etapa2', 'auditores', 'iaf_md4_confirmado', 'estado'
        ]

    def clean_fecha_programacion_etapa2(self):
        fechas = self.cleaned_data['fecha_programacion_etapa2']
        if fechas:
            fechas_lista = [fecha.strip() for fecha in fechas.split(",") if fecha.strip()]
            if len(fechas_lista) > 3:
                raise forms.ValidationError("No puedes ingresar más de 3 fechas para la etapa 2.")
            return fechas_lista
        return []
