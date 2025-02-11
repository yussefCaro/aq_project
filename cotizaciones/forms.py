from django import forms
from .models import Cotizacion, TipoServicio

class CotizacionForm(forms.ModelForm):
    tipo_servicio = forms.ModelMultipleChoiceField(
        queryset=TipoServicio.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )

    precio_iva = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False,
        widget=forms.HiddenInput()  #  Cambiado a HiddenInput
    )

    precio_total = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False,
        widget=forms.HiddenInput()  #  Cambiado a HiddenInput
    )

    class Meta:
        model = Cotizacion
        fields = ['numero_servicio', 'tipo_servicio', 'precio_neto', 'precio_iva', 'precio_total']

