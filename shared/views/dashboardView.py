import os
import fnmatch

def buscar_dashboards(root_folder, pattern):
    dashboards = []
    # Recorremos todos los directorios a partir del directorio raíz
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in fnmatch.filter(filenames, pattern):
            # Se guarda la ruta completa del archivo
            dashboards.append(os.path.join(dirpath, filename))
    return dashboards

from django.shortcuts import render
from django.conf import settings

def dashboard_selector(request):
    # Ruta al directorio del proyecto Django
    root_folder = settings.BASE_DIR  # Utiliza BASE_DIR para obtener la ruta del proyecto
    pattern = 'dashView_*'
    
    # Buscar dashboards
    dashboards = buscar_dashboards(root_folder, pattern)
    
    # Extraer solo los nombres de archivo sin la ruta completa
    dashboard_names = [os.path.basename(dashboard) for dashboard in dashboards]
    
    return render(request, 'dashboard/selector.html', {'dashboards': dashboard_names})
