from django import forms
from .models import ProgramacionAuditoria

class ProgramacionAuditoriaForm(forms.ModelForm):
    fecha_programacion_etapa2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Fechas separadas por comas'}))

    class Meta:
        model = ProgramacionAuditoria
        fields = [
            "fecha_programacion_etapa1",
            "fecha_programacion_etapa2",
            "hora_etapa1",
            "hora_etapa2",
            "iaf_md4_confirmado",
            "estado",
        ]

    def clean_fecha_programacion_etapa2(self):
        """Convierte el texto separado por comas en una lista."""
        fechas = self.cleaned_data["fecha_programacion_etapa2"]
        return [fecha.strip() for fecha in fechas.split(",")]
