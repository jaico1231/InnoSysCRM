
from shared.mixins import *
from MacroProcesos.models.macroprocesos import *
from MacroProcesos.forms.macro_procesos_form import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

    
class Listar_MacroProcesos(LoginRequiredMixin, PermissionRequiredMixin, MenuMixin, ListView):
    permission_required = 'MacroProcesos.view_macroprocesos'
    model = MacroProcesos
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configuracion de MacroProcesos'
        context['entity'] = 'MacroProcesos'
        context['Btn_Add'] = [
            {
                'name':'add',
                'label':'Crear MacroProcesos',                
                'url':'macroprocesos:Crear_MacroProcesos',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['IDENTIFICADOR', 'MACRO PROCESO', 'OBSERVACION']  # Encabezados de columnas
        context['fields'] = ['IdMacroProcesos', 'MacroProcesos', 'Observacion']  # Campos del modelo
        context['actions'] = [

            {
                'name': 'edit',
                'label': '',
                'icon': 'edit',
                'color': 'secondary',
                'color2': 'brown',
                'url': 'macroprocesos:Editar_MacroProcesos',
                'modal': 'Activar',
                
            },
            {
                'name': 'delete',
                'label': '',
                'icon': 'delete',
                'color': 'danger',
                'color2': 'white',
                'url': 'macroprocesos:Eliminar_MacroProcesos',
                'modal': 'Activar',
            },
            # Agrega más acciones aquí sea necesario
        ]
        return context

class Crear_MacroProcesos(LoginRequiredMixin, PermissionRequiredMixin, SuccessUrlMixin,CreateView):
    permission_required = 'MacroProcesos.add_macroprocesos'
    model = MacroProcesos
    form_class = Macro_Procesos_Form
    template_name = 'shared/create.html'
    success_url = reverse_lazy('macroprocesos:Listar_MacroProcesos')
        
    def form_valid(self, form):
        macroproceso = form.cleaned_data.get('MacroProcesos')
        log_event(self.request.user, "info", f"Se Creo el MacroProcesos. {macroproceso}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear MacroProcesos'
        context['entity'] = 'MacroProcesos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_MacroProcesos')
        context['cancel_url'] = reverse_lazy('macroprocesos:Listar_MacroProcesos')
        return context
    
class Editar_MacroProcesos(LoginRequiredMixin, PermissionRequiredMixin, SuccessUrlMixin, UpdateView):
    permission_required = 'MacroProcesos.change_macroprocesos'
    model = MacroProcesos
    form_class = Macro_Procesos_Form
    template_name = 'shared/create.html'
    success_url = reverse_lazy('macroprocesos:Listar_MacroProcesos')

    def form_valid(self, form):
        macroproceso = form.cleaned_data.get('MacroProcesos')
        log_event(self.request.user, "info", f"Se Edito el MacroProcesos. {macroproceso}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar MacroProcesos'
        context['entity'] = 'MacroProcesos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_MacroProcesos')
        return context
    
class Eliminar_MacroProcesos(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'MacroProcesos.delete_macroprocesos'
    model = MacroProcesos
    template_name = 'shared/del.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('macroprocesos:Listar_MacroProcesos')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        MacroProceso = MacroProcesos.objects.get(IdMacroProcesos=self.object.IdMacroProcesos)
        log_event(self.request.user, "info", f"Se eliminó el macroproceso {MacroProceso}.")
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar MacroProcesos'
        context['texto'] = f'Seguro de eliminar el MacroProceso {self.object.MacroProcesos}?'  # Asegúrate de que 'nombre' sea el campo adecuado
        context['entity'] = 'MacroProcesos'
        context['list_url'] = reverse_lazy('macroprocesos:Listar_MacroProcesos')
        return context