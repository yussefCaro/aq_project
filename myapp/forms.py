from django import forms


class CreateNewTask(forms.Form):
    title = forms.CharField(label="Titulo de la Tarea", max_length=100,
                            widget=forms.TextInput(attrs={'class': 'input'}))
    description = forms.CharField(label="Descripción de la Tarea", widget=forms.Textarea(attrs={'class': 'input'}))


class CreateNewProject(forms.Form):
    name = forms.CharField(label="Crear un nuevo Proyecto", max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))
