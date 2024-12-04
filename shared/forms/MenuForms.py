from django import forms

from shared.models.menu import Menu, MenuItem

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'group', 'icon']
        labels = {
            'name': 'Nombre', 
            'group': 'Grupo', 
            'icon': 'Icono'
            }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'icon': forms.Select(attrs={'class': 'form-control'}),
            }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['menu','name', 'url_name', 'icon','groups', 'estado']
        labels = {
            'menu': 'Menu Categoria',
            'name': 'Nombre', 
            'url_name': 'Url', 
            'icon': 'Icono',
            'groups': 'Permisos',
            'estado': 'Activo'
            }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url_name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'menu': forms.Select(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'style': 'width: 20px; height: 20px;'}),


            }
        