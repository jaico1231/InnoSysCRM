import os
import shutil
from pathlib import Path
import django
from django.core.management import call_command
from importlib import import_module

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ROMIL_BETA1.settings')
django.setup()

from django.conf import settings

# Definir el directorio base de tu proyecto
BASE_DIR = Path(__file__).resolve().parent

def borrar_migraciones():
    """Elimina los archivos de migración de todas las aplicaciones locales."""
    for app in settings.INSTALLED_APPS:
        if app.startswith('django.') or app.startswith('rest_framework'):
            continue

        # Obtener la ruta de migraciones para la aplicación
        try:
            app_path = Path(import_module(app).__file__).parent
            migraciones_path = app_path / 'migrations'

            if migraciones_path.exists():
                print(f"Borrando migraciones en {migraciones_path}")
                shutil.rmtree(migraciones_path)
                os.makedirs(migraciones_path)
                # Crear un archivo __init__.py vacío en el directorio de migraciones
                with open(migraciones_path / '__init__.py', 'w'):
                    pass
        except ModuleNotFoundError:
            print(f"El módulo {app} no tiene directorio o no es válido.")
        except Exception as e:
            print(f"Error al eliminar migraciones para {app}: {e}")

def reiniciar_base_de_datos():
    """Elimina y recrea la base de datos, y aplica las migraciones iniciales."""
    # Borrar la base de datos existente
    db_path = BASE_DIR / 'db.sqlite3'  # Ajusta esto según tu configuración de base de datos
    if db_path.exists():
        print(f"Borrando la base de datos en {db_path}")
        os.remove(db_path)
    
    # Crear nuevas migraciones
    print("Creando nuevas migraciones")
    call_command('makemigrations')
    
    # Aplicar migraciones a la nueva base de datos
    print("Aplicando migraciones a la nueva base de datos")
    call_command('migrate')

def ejecutar_utils():
    """Ejecutar las inicializaciones de datos para todas las aplicaciones locales."""
    for app in settings.INSTALLED_APPS:
        if app.startswith('django.') or app.startswith('rest_framework'):
            continue

        try:
            # Intentar importar el módulo 'utils' de la aplicación
            app_module = import_module(f'{app}.utils')
            
            # Buscar la función 'datos_iniciales_<app>'
            func_name = f'datos_iniciales_{app.split(".")[-1].lower()}'
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

if __name__ == "__main__":
    borrar_migraciones()
    reiniciar_base_de_datos()
    print("Base de datos reiniciada exitosamente.")
    print("Configurando el entorno de Django...")
    ejecutar_utils()
    print("Datos cargados exitosamente.")
