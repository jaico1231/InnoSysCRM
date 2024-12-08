
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm
from shared.models.user import User
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'groups','TipoDocumento', 'image', 'NumeroIdentificacion']
        exclude = ['password1', 'password2', 'last_login', 'is_superuser',  'user_permissions', 'is_staff', 'is_active', 'date_joined' ]
                  
        labels = {
            'TipoDocumento': 'Tipo Documento',
            'groups': 'Grupo de Usuarios',

        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'NumeroIdentificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'TipoDocumento': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),

        }
        def save(self, commit=True):
            data = {}
            try:
                if self.is_valid():
                    super().save()
                else:
                    data['error'] = self.errors
            except Exception as e:
                data['error'] = str(e)
            return data
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name',
            'last_name',
            'email',
            'TipoDocumento',
            'image',
            'NumeroIdentificacion',
            'last_login',
            'groups',
            'user_permissions',
            'date_joined'
            ]
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Email',
            'TipoDocumento': 'Tipo Documento',
            'image': 'Imagen',
            'NumeroIdentificacion': 'Número de identificación',
            'last_login': 'Último inicio de sesión',
            'groups': 'Grupos',
            'user_permissions': 'Permisos de usuario',
            'date_joined': 'Fecha de registro'            
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'TipoDocumento': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'NumeroIdentificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'last_login': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'user_permissions': forms.SelectMultiple(attrs={'class': 'form-control' 'multiple' }),
            'date_joined': forms.TextInput(attrs={'class': 'form-control'}),
            
        }


class ChangePasswordForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": _(
            "La contraseña que ha introducido no es correcta.Inténtelo de nuevo."
        ),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password

class RenewPasswordForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['password']
        labels = {
            'password': 'Contraseña nueva',
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }