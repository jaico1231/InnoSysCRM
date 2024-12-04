from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from shared.loggin import log_event

class ToggleEstadoView(LoginRequiredMixin, UpdateView):
    model = None  # Esto se definirá dinámicamente en cada caso
    fields = []  # El campo que se va a modificar se definirá dinámicamente
    success_url = None  # Esto también se establecerá dinámicamente

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        # Obtenemos el objeto de acuerdo al 'pk' y el modelo especificado
        model_instance = self.get_object()
        
        # Verificamos que el campo 'estado' exista en el modelo
        if not hasattr(model_instance, self.fields[0]):
            return JsonResponse({'success': False, 'message': 'El campo no existe en el modelo.'}, status=400)
        
        # Invertir el valor del campo (activado/desactivado)
        current_value = getattr(model_instance, self.fields[0])
        setattr(model_instance, self.fields[0], not current_value)
        model_instance.save()
        
        # Opcional: Registrar un log de la acción
        log_event(request.user, self.model._meta.model_name, f"Se cambió el valor de {self.fields[0]} de {current_value} a {not current_value}")
        
        # Devolver la respuesta en formato JSON
        return JsonResponse({'success': True, self.fields[0]: not current_value})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Activar/Desactivar {self.model._meta.verbose_name}'
        context['entity'] = self.model._meta.verbose_name
        context['list_url'] = reverse_lazy(f'{self.model._meta.app_label}:{self.model._meta.model_name}list')
        return context

    def get_object(self):
        """ Permite obtener el objeto de acuerdo al 'pk' con el modelo dinámico """
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

