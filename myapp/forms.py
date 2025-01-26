from django import forms
from django.forms import ModelForm
from .models import Task


class TaskForm (forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'project']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'descripción' }),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CreateNewProject(forms.Form):
    name = forms.CharField(label="Crear un nuevo Proyecto", max_length=100,
                           widget=forms.TextInput(attrs={'class': 'input'}))
