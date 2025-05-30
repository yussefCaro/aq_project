from django.forms import ValidationError, BaseModelFormSet
from ejecucion_auditoria.models import EjecucionRequisito
from django import forms

class EjecucionBaseFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        # Solo valida si se activa el flag desde la vista
        if getattr(self, 'validar_completo', False):
            for i, form in enumerate(self.forms):
                if not form.cleaned_data.get('DELETE', False):
                    campos_obligatorios = [campo for campo in ['cumple', 'no_cumple', 'no_aplica'] if campo in form.cleaned_data]

                    if not any(form.cleaned_data.get(campo) for campo in campos_obligatorios):
                        raise ValidationError(
                            f"Fila {i+1} sin diligenciar: debe marcar al menos una opción (Cumple, No Cumple o No Aplica)."
                        )

class EjecucionRequisitoForm(forms.ModelForm):

    class Meta:
        model = EjecucionRequisito
        fields = [
            'cumple', 'no_cumple', 'no_aplica',
            'aspecto_mejora', 'concepto_mejora',
            'concepto_no_conformidad', 'evidencia',
            'concepto_evidencia', 'imagen1', 'imagen2',
            'subsanado', 'como_se_subsano'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['concepto_no_conformidad'].widget.attrs['style'] = 'background:#f8f9fa;'

        # Solo agrega atributos si el campo está presente en el formulario
        if 'no_cumple' in self.fields:
            self.fields['no_cumple'].widget.attrs.update({
                'class': 'form-check-input no-cumple-checkbox mutuamente-excluyente',
                'data-target': f'no-conformidad-{self.prefix}'
            })

        if 'aspecto_mejora' in self.fields:
            self.fields['aspecto_mejora'].widget.attrs.update({
                'class': 'form-check-input aspecto-mejora-checkbox mutuamente-excluyente',
                'data-target': f'mejora-{self.prefix}'
            })

        if 'evidencia' in self.fields:
            self.fields['evidencia'].widget.attrs.update({
                'class': 'form-select evidencia-select',
                'data-target': f'evidencia-concepto-{self.prefix}'
            })


