from django import forms
from .models import Cliente, Producto

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

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'num_habitaciones', 'num_banios', 'num_plantas', 'pared_m2', 'suelo_m2', 'tejado_m2', 'espesores', 'tipo_productos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el nombre'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el precio'}),
            'num_habitaciones': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el número de habitaciones'}),
            'num_banios': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el número de baños'}),
            'num_plantas': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el número de plantas'}),
            'pared_m2': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'pared_m2'}),
            'suelo_m2': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'suelo_m2'}),
            'tejado_m2': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'tejado_m2'}),
            'espesores': forms.CheckboxInput(attrs={'class': 'form-control p-2 m-1'}),
            'tipo_productos': forms.CheckboxInput(attrs={'class': 'form-control p-2 m-1'}),
        }
        labels = {
            'num_habitaciones': 'Número de habitaciones',
            'num_banios': 'Número de baños',
            'num_plantas': 'Número de plantas',
            'tipo_productos': 'Tipo de producto',
        }
