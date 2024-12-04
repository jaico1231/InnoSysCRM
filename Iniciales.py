import os
import django
from importlib import import_module

# Configura la variable de entorno antes de importar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InnoSysCRM.settings')  # Cambia 'ROMIL_01.settings' por tu configuración correcta
django.setup()

from django.conf import settings

# Función para ejecutar la inicialización de todas las aplicaciones
def ejecutar_utils():
    for app in settings.INSTALLED_APPS:
        # Ignorar aplicaciones de Django y otras que no sean relevantes
        if app.startswith('django.') or app.startswith('rest_framework'):
            continue

        try:
            # Intentar importar el módulo 'utils' de la aplicación
            app_module = import_module(f'{app}.utils')
            
            # Buscar la función 'datos_iniciales_<app>' en el módulo 'utils'
            func_name = f'datos_iniciales_{app.split(".")[-1].lower()}'  # Crear nombre de la función esperado
            if hasattr(app_module, func_name):
                init_function = getattr(app_module, func_name)
                print(f"Ejecutando {func_name} en {app}")
                init_function()
            else:
                print(f"No se encontró la función {func_name} en {app}")
                
        except ModuleNotFoundError:
            print(f"No se encontró el módulo 'utils' en {app}")
        except Exception as e:
            print(f"Error ejecutando {app}: {e}")

# Ejecutar inicializaciones
ejecutar_utils()
