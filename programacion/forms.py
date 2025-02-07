from django import forms
from .models import Programacion

class ProgramacionForm(forms.ModelForm):
    class Meta:
        model = Programacion
        fields = ['fecha_auditoria', 'auditor']
        widgets = {
            'fecha_auditoria': forms.DateInput(attrs={'type': 'date'}),
        }
