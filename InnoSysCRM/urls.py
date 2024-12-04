"""
URL configuration for DiagnostikaApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# Definición del decorador para añadir el nombre del menú
from functools import wraps

def add_menu_name(menu_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            # Aquí puedes agregar lógica adicional si es necesario
            return view_func(*args, **kwargs)        
        _wrapped_view.menu_name = menu_name  # Agregar el atributo menu_name
        return _wrapped_view
    return decorator

import functools
def print_module(view_func):
    @functools.wraps(view_func)
    def wrapped_view(*args, **kwargs):
        module_name = view_func.__module__
        print(f"La vista '{view_func.__name__}' pertenece al módulo: {module_name}")
        return view_func(*args, **kwargs)
    return wrapped_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shared.urls')),
    path('', include('configuracion.urls')),
    path('', include('ventas.urls')),
    path('', include('informes.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)