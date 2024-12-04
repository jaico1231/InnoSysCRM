from django.contrib.auth.management.commands.changepassword import UserModel
from django import forms
from shared.models.user import User

class AutenticationForm(forms.Form):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {'username': 'Usuario', 'password': 'Contraseña'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Ingrese usuario'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Ingrese contraseña'}),
        }
        
