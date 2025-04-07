from django import forms
from django.contrib.auth.models import User
from .models import Profile, Rol

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset = Rol.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )
    class Meta:
        model = Profile
        fields = ['telefono', 'roles', 'fecha_nacimiento', 'imagen']
