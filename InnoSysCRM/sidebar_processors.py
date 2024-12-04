from pathlib import Path
import glob
from .settings import BASE_DIR

#menu por base de datos
from django.shortcuts import render
from shared.models.menu import Menu, MenuItem

def sidebar_context(request):
    menus = Menu.objects.filter(estado=True)
    menu_items = MenuItem.objects.filter(estado=True)

    # Filtrar menús según los permisos del usuario
    if not request.user.is_superuser:
        user_groups = request.user.groups.all()
        menus = menus.filter(group__in=user_groups)

    return {
        'menus': menus,
        'menu_items': menu_items
    }

