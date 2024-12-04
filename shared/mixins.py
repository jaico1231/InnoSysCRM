from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML, CSS
import os
# ###################################################################################
from django.views.generic import *
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from shared.models.menu import *
from shared.loggin import log_event
from django.urls import reverse, reverse_lazy
from urllib import response

class PDFTemplateMixin:
    pdf_template_name = None  # Template que será usado para generar el PDF

    def get_pdf_template_name(self):
        """Devuelve el nombre del template. Sobrescribe este método si necesitas lógica personalizada."""
        if self.pdf_template_name is None:
            raise ValueError("Debes definir 'pdf_template_name' en la vista o en la subclase.")
        return self.pdf_template_name

    def get_context_data(self, **kwargs):
        """Sobrescribe este método para agregar datos adicionales al contexto."""
        return kwargs

    def get_pdf_stylesheets(self):
        """Devuelve una lista de hojas de estilo (CSS) para aplicar al PDF."""
        # Puedes definir una hoja de estilo personalizada
        stylesheet_path = os.path.join(os.path.dirname(__file__), 'static/css/pdf_styles.css')
        if os.path.exists(stylesheet_path):
            return [CSS(stylesheet_path)]
        return []

    def render_to_pdf(self, context=None):
        """
        Genera un archivo PDF a partir de un contexto y un template HTML.
        """
        if context is None:
            context = {}

        # Obtener el template HTML
        template = get_template(self.get_pdf_template_name())
        html_content = template.render(context)

        # Crear el PDF usando WeasyPrint
        pdf_file = HTML(string=html_content).write_pdf(stylesheets=self.get_pdf_stylesheets())

        # Retornar el archivo PDF
        return pdf_file

    def get(self, request, *args, **kwargs):
        """
        Método GET que genera el PDF cuando es llamado desde la vista.
        """
        # Obtener el contexto (normalmente proviene de la vista)
        context = self.get_context_data(**kwargs)

        # Renderizar el PDF
        pdf = self.render_to_pdf(context)

        # Retornar una respuesta HTTP con el PDF como adjunto
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{self.get_pdf_filename()}"'
        return response

    def get_pdf_filename(self):
        """Devuelve el nombre del archivo PDF."""
        return 'documento.pdf'

class SuccessUrlMixin:
    success_url = None
    def get_success_url(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            return HttpResponseRedirect(self.get_success_url())
class DelUrlMixin:        
    def del_get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return HttpResponseRedirect(self.del_get_success_url())
class MenuMixin:
    def get_menu_items(self):
        return Menu.objects.prefetch_related('menu_items').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = self.get_menu_items()
        return context

    def get_success_url(self):
        if hasattr(self, 'success_url_name'):
            return reverse(self.success_url_name)
        raise ImproperlyConfigured('No URL to redirect to. Provide a success_url or success_url_name.')