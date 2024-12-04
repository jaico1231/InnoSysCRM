from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group
from shared.models.menu import Menu, MenuItem  # Asegúrate de que los modelos estén importados correctamente
from django.urls import get_resolver, URLPattern, URLResolver


class Command(BaseCommand):
    help = 'Crea menús y ítems de menú automáticamente basados en las vistas disponibles'

    def handle(self, *args, **kwargs):
        print("Iniciando la creación de menús y elementos de menú...")  # Mensaje inicial
        
        local_apps = settings.LOCAL_APPS
        
        for app_label in local_apps:
            print(f"Procesando la aplicación: {app_label}")  # Indicar la aplicación actual
            
            app_config = apps.get_app_config(app_label)
            menu_name = 'ADMINISTRACION' if app_label == 'shared' else app_label.upper()
            
            # Crear o obtener el grupo y el menú
            group, created_group = Group.objects.get_or_create(name=app_label)
            print(f"Grupo {'creado' if created_group else 'existente'}: {group.name}")

            menu, created_menu = Menu.objects.get_or_create(name=menu_name)
            admin_group_instance, _ = Group.objects.get_or_create(name='Administrador')  # Obtener o crear el grupo "Administrador"
            
            menu.group.add(admin_group_instance)  # Agregar el grupo "Administrador" al menú
            print(f"Menú {'creado' if created_menu else 'existente'}: {menu.name}")

            # Llamar a la función para extraer e imprimir las rutas
            self.print_menu_paths(app_label)

    def print_menu_paths(self, app_name):
        print(f"URLs para el menú '{app_name}':")
        urlconf = get_resolver()  # Obtiene el resolutor de URLs
        urlpatterns = urlconf.url_patterns
        
        def extract_paths(urlpatterns, prefix=''):
            for pattern in urlpatterns:
                if isinstance(pattern, URLPattern):
                    menu_name = getattr(pattern.callback, 'menu_name', None)
                    url_str = str(pattern)  # Convertir el patrón a cadena
                    if pattern.name is not None and menu_name is not None:
                        module_name = pattern.callback.__module__.split('.')[-3]  # Extraer el nombre de la app
                        menus = Menu.objects.filter(name=module_name)

                        # Verificar si se encontraron menús
                        if menus.exists():
                            id_menu = menus.first().id  # Obtener el ID del primer menú encontrado
                        else:
                            print(f"No se encontró ningún menú para el módulo: {module_name}")
                            continue  # Salir del bucle si no hay menú

                        grupos = Group.objects.filter(name='Administrador')
                        

                        # Crear el MenuItem
                        menuitem, created_menuitem = MenuItem.objects.get_or_create(
                            menu=Menu.objects.get(id=id_menu),
                            name=menu_name,
                            url_name=f'{prefix}{pattern.name}',
                        )

                        if created_menuitem:
                            print(f"SE CREO EL MENUITEM: {menuitem.name} EN EL MENU: {menuitem.menu.name}")
                        else:
                            print(f"EL MENUITEM YA EXISTE: {menuitem.name} EN EL MENU: {menuitem.menu.name}")

                elif isinstance(pattern, URLResolver):
                    extract_paths(pattern.url_patterns, prefix + (pattern.app_name + ':') if pattern.app_name else '')

        extract_paths(urlpatterns)