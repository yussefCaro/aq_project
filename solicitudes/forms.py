from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nit': forms.TextInput(attrs={'placeholder': 'Nit del cliente'}),
            'telefono_fijo': forms.TextInput(attrs={'placeholder': 'Teléfono Fijo (opcional)'}),
            # Agregar widgets para los campos necesarios
        }

class SolicitudForm(forms.Form):
    nit = forms.CharField(max_length=50)
    propietario = forms.CharField(max_length=100)
    establecimiento_comercial = forms.CharField(max_length=100)
    representante_legal = forms.CharField(max_length=100)
    cedula = forms.CharField(max_length=50)
    ciudad = forms.CharField(max_length=100)
    departamento = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=200)
    representante_organismo = forms.CharField(max_length=100)
    cargo = forms.CharField(max_length=50)
    telefono_fijo = forms.CharField(max_length=50, required=False)
    telefono_celular = forms.CharField(max_length=50)
    correo = forms.EmailField()
    nivel_cea = forms.ChoiceField(choices=[('1', 'Nivel 1'), ('2', 'Nivel 2'), ('3', 'Nivel 3'), ('3_instructores', 'Nivel 3 con Formación de Instructores')])
    cantidad_vehiculos = forms.IntegerField()
    cantidad_instructores = forms.IntegerField()
    ente_certificador = forms.ChoiceField(choices=[('si', 'Sí'), ('no', 'No')])
    nombre_ente_certificador = forms.CharField(max_length=100, required=False)