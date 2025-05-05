from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo', 'ciudad', 'fecha_contacto', 'nota', 'via_entrada', 'comercial', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el nombre'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el correo'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe la ciudad'}),
            'fecha_contacto': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'nota': forms.Textarea(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe una nota'}),
            'via_entrada': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe la via de entrada'}),
            'comercial': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'estado': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
        }
        labels = {
            'fecha_contacto': 'Fecha de contacto',
            'via_entrada': 'Vía de entrada',
        }