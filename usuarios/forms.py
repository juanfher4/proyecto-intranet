from django import forms
from django.contrib.auth.models import User
from .models import Profile, Rol

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe tu nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe tu email'}),
        }

class ProfileEditForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset = Rol.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )
    class Meta:
        model = Profile
        fields = ['telefono', 'roles', 'fecha_nacimiento', 'imagen']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe tu número de teléfono'}),
            'roles': forms.CheckboxInput(attrs={'class': 'form-control p-2 m-1'}),
            'fecha_nacimiento': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control p-2 m-1'}),
        }
