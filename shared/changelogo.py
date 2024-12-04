import os
import re
def update_base_html(logo_url):
    # Ruta al archivo base.html
    base_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'layout', 'base.html')

    # Leer el contenido del archivo base.html
    with open(base_html_path, 'r') as file:
        content = file.read()

    # Definir la nueva línea del logo
    if logo_url:
        # Formateamos la cadena de texto primero
        logo_url = '{% static \'' + logo_url + '\' %}'
        new_logo_line = f'<img src="{logo_url}" width="180" alt="Logo" />'
    else:
        new_logo_line = '<img src="{% static \'assets/img/logos/sin_logo.png\' %}" width="180" alt="Sin logo" />'

    # Modificar el contenido reemplazando solo la línea del logo
    updated_content = re.sub(r'<img src=".*?width="180" alt=".*?" />', new_logo_line, content)

    # Escribir el contenido actualizado de vuelta al archivo base.html
    with open(base_html_path, 'w') as file:
        file.write(updated_content)


# def update_base_html(logo_url):
#     # Ruta al archivo base.html
#     base_html_path = os.path.join(os.path.dirname(__file__),  'templates', 'layout', 'base.html')

#     # Leer el contenido del archivo base.html
#     with open(base_html_path, 'r') as file:
#         content = file.read()

#     # Reemplazar la URL del logo en el archivo
#     new_logo_line = f'<img src=" static assets/{logo_url}" width="180" alt="Logo" />' if logo_url else '<img src="{% static \'assets/img/logos/sin_logo.png\' %}" width="180" alt="Sin logo" />'
#     # <img src="{% static 'assets/img/logos/sin_logo.png' %}" width="180" alt="" />
#     # Modificar el contenido
#     updated_content = re.sub(r'<img src=".*" width="180" alt=".*" />', new_logo_line, content)

#     # Escribir el contenido actualizado de vuelta al archivo base.html
#     with open(base_html_path, 'w') as file:
#         file.write(updated_content)
