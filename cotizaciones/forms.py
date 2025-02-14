from django import forms
from .models import Cotizacion, TipoServicio

class CotizacionForm(forms.ModelForm):
    tipo_servicio = forms.ModelMultipleChoiceField(
        queryset=TipoServicio.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )

    precio_iva = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, disabled=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    precio_total = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, disabled=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    estado = forms.ChoiceField(
        choices=Cotizacion.ESTADO_CHOICES,
        widget=forms.Select(),
        required=True
    )



    class Meta:
        model = Cotizacion
        fields = ['numero_servicio', 'tipo_servicio', 'precio_neto', 'precio_iva', 'precio_total', 'estado','fecha_cotizacion' ]

