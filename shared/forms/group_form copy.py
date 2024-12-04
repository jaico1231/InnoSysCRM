# forms.py
from django import forms
from django.contrib.auth.models import Group, Permission

class GroupForm(forms.ModelForm):
    permissions_from = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),  # Todos los permisos
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '10'
        })
    )
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {
            'name': 'Nombre del Grupo',
            'permissions': 'Permisos'
        }
        widgets = {
            'permissions': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '10'
            }),
            'permissions_from': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '10'
            })
        }



# class GroupForm(forms.ModelForm):
#     # Permisos no seleccionados
#     permissions_from = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),  # Todos los permisos
#         required=False,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'form-control',
#             'size': '10'
#         })
#     )
    
#     # Permisos seleccionados
#     permissions_to = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.none(),  # Inicialmente vacío
#         required=False,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'form-control',
#             'size': '10'
#         })
#     )

#     class Meta:
#         model = Group
#         fields = ['name', 'permissions_from', 'permissions_to']
#         labels = {
#             'name': 'Nombre del Grupo',
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         if self.instance.pk:
#             # Permisos que ya están seleccionados para el grupo
#             selected_permissions = self.instance.permissions.all()
#             # Permisos que no están seleccionados
#             available_permissions = Permission.objects.exclude(id__in=selected_permissions.values_list('id', flat=True))

#             # Asignar los permisos al queryset correcto
#             self.fields['permissions_from'].queryset = available_permissions
#             self.fields['permissions_to'].queryset = selected_permissions
#         else:
#             # Si es un nuevo grupo, todos los permisos están disponibles
#             self.fields['permissions_from'].queryset = Permission.objects.all()

#     def save(self, commit=True):
#         group = super().save(commit=False)
#         if commit:
#             group.save()
#             # Limpiar permisos existentes
#             group.permissions.clear()
#             # Asignar permisos seleccionados
#             selected_permissions = self.cleaned_data.get('permissions_to', [])
#             # Verificar que los permisos seleccionados sean válidos
#             valid_permissions = Permission.objects.filter(id__in=[perm.id for perm in selected_permissions])
#             group.permissions.set(valid_permissions)
#         return group

# class GroupForm(forms.ModelForm):
#     # Permisos no seleccionados
#     permissions_from = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),  # Todos los permisos
#         required=False,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'form-control',
#             'size': '10'
#         })
#     )
    
#     # Permisos seleccionados
#     permissions_to = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.none(),  # Inicialmente vacío
#         required=False,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'form-control',
#             'size': '10'
#         })
#     )

#     class Meta:
#         model = Group
#         fields = ['name', 'permissions_from', 'permissions_to']
#         labels = {
#             'name': 'Nombre del Grupo',
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         if self.instance.pk:
#             # Permisos que ya están seleccionados para el grupo
#             selected_permissions = self.instance.permissions.all()
#             # Permisos que no están seleccionados
#             available_permissions = Permission.objects.exclude(id__in=selected_permissions)

#             # Asignar los permisos al queryset correcto
#             self.fields['permissions_from'].queryset = available_permissions
#             self.fields['permissions_to'].queryset = selected_permissions
#         else:
#             # Si es un nuevo grupo, todos los permisos están disponibles
#             self.fields['permissions_from'].queryset = Permission.objects.all()

        

# class GroupForm(forms.ModelForm):
#     # Permisos no seleccionados
#     permissions_from = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),  # Todos los permisos
#         required=False,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'form-control',
#             'size': '10'
#         })
#     )
    
#     # Permisos seleccionados
#     permissions_to = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.none(),  # Inicialmente vacío
#         required=False,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'form-control',
#             'size': '10'
#         })
#     )

#     class Meta:
#         model = Group
#         fields = ['name', 'permissions_from', 'permissions_to']
#         labels = {
#             'name': 'Nombre del Grupo',
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         if self.instance.pk:
#             # Permisos que ya están seleccionados para el grupo
#             selected_permissions = self.instance.permissions.all()
#             # Permisos que no están seleccionados
#             available_permissions = Permission.objects.exclude(id__in=selected_permissions)

#             # Asignar los permisos al queryset correcto
#             self.fields['permissions_from'].queryset = available_permissions
#             self.fields['permissions_to'].queryset = selected_permissions
#         else:
#             # Si es un nuevo grupo, todos los permisos están disponibles
#             self.fields['permissions_from'].queryset = Permission.objects.all()
