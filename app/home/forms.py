from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control p-2 m-2', 'placeholder': 'Escribe un título'}),
            'description': forms.Textarea(attrs={'class': 'form-control p-2 m-2', 'placeholder': 'Escribe una descripción'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'important': '¿Es importante?',
        }
