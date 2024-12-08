
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ActivosFijos.models.articulos import Articulo
from ActivosFijos.models.anexo_articulo import Anexos_Articulos
from ActivosFijos.models.hoja_vida_articulo import Hoja_Vida_Articulos
from ActivosFijos.forms import ArticuloForm, Anexos_ArticuloForm
from shared.loggin import log_event

class Listar_ArticulosView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'ActivosFijos.view_articulo'
    model = Articulo
    template_name = 'shared/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Articulos'
        context['entity'] = 'Articulos'
        context['Btn_Add'] = [
            {
                'url':'ACTIVOS:Crear_ART',
                'modal': 'Activar',
            }
        ]
        context['headers'] = ['CODIGO', 'DESCRIPCION', 'GRUPO','MARCA','MODELO']  # Encabezados de columnas
        context['fields'] = ['codigo', 'Descripcion', 'GrupoArticulo_FK','Marca_FK','Modelo']  # Campos del modelo
        context['actions'] = [
            {
                'name': 'edit', 
                'label': '', 
                'icon': 'edit', 
                'color': 'secondary', 
                'color2': 'brown', 
                'url': 'ACTIVOS:Editar_ART',
                'modal': 'Activa'
            },
            {
                'name': 'delete', 
                'label': '', 
                'icon': 'delete', 
                'color': 'danger',
                'color2': 'white', 
                'url': 'ACTIVOS:Borrar_ART',
                'modal': 'Activa'
            },
        ]
        return context
class Crear_ArticulosView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'ActivosFijos.add_articulo'
    model = Articulo
    form_class = ArticuloForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_ART')
    
    def form_valid(self, form):
        articulo = form.save(commit=False)
        articulo.save()
        log_event(self.request.user,'info', f'Se creo el Articulo {articulo}')
        #se creara la hoja de vida del articulo automaticamente genera el codigo 
        hoja_vida=Hoja_Vida_Articulos.objects.get_or_create(Articulo_FK=articulo)
        hoja_vida.save()
        # Hoja_Vida_Articulos.objects.get_or_create(Articulo_FK=articulo)
        # se crea el anexo del articulo
        
        anexos_form = Anexos_ArticuloForm(self.request.POST, self.request.FILES, instance=articulo.anexos_articulos_set.first() if articulo.anexos_articulos_set.exists() else None)
        # anexos_form = Anexos_ArticuloForm(self.request.POST, self.request.FILES, instance=Articulo.Anexos_Articulos.first())
        if anexos_form.is_valid():
            anexos = anexos_form.save(commit=False)
            anexos.IdArticuloFK = articulo
            anexos.save()
            log_event(self.request,'info', f'Se agrego un anexo al Articulo {articulo}')
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            anexos_form = Anexos_ArticuloForm(instance=self.object.Anexos_Articulos.first())
        else:
            anexos_form = Anexos_ArticuloForm()
        context['anexos_form'] = anexos_form
        context['title'] = 'Crear Artículo'
        context['entity'] = 'Artículos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_ART')
        return context

    

class Editar_ArticulosView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'ActivosFijos.change_articulo'
    model = Articulo
    form_class = ArticuloForm
    template_name = 'shared/create.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_ART')
    
    def form_valid(self, form):
        # context = self.get_context_data()
        articulo = form.save()
        log_event(self.request.user,'info', f'Se edito el Articulo {articulo}')
        anexos_form = Anexos_ArticuloForm(self.request.POST, self.request.FILES, instance=articulo.anexos_articulos_set.first() if articulo.anexos_articulos_set.exists() else None)
        # anexos_form = context['anexos_form']
        if anexos_form.is_valid():
            anexo = anexos_form.save(commit=False)
            anexo.IdArticuloFK = form.instance
            anexo.save()
            log_event(self.request,'info', f'Se agrego un anexo al Articulo {articulo}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # articulo = self.get_object()
        # anexos = Anexos_Articulos.objects.filter(IdArticuloFK=articulo)
        # context['anexos'] = anexos
        # context['anexos_form'] = Anexos_ArticuloForm()
        context['title'] = 'Editar Articulos'
        context['entity'] = 'Articulos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_ART')
        return context

    
# class Editar_ArticulosView(UpdateView):
#     model = Articulo
#     form_class = ArticuloForm
#     template_name = 'Articulos/Detalle_Articulos3.html'
#     success_url = reverse_lazy('ACTIVOS:Listar_ART')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         articulo = self.get_object()
#         anexo = Anexos_Articulos.objects.filter(IdArticuloFK=articulo).first()
#         print(anexo)
#         if anexo:
#             context['anexos_form'] = Anexos_ArticuloForm(instance=anexo)
#         else:
#             context['anexos_form'] = Anexos_ArticuloForm()
        
#         context['title'] = 'Editar Articulos'
#         context['entity'] = 'Articulos'
#         context['list_url'] = reverse_lazy('ACTIVOS:Listar_ART')
#         return context
  

#     def form_valid(self, form):
#         articulo = form.save()
#         anexos_form = Anexos_ArticuloForm(self.request.POST, self.request.FILES, instance=articulo.anexos_articulos_set.first() if articulo.anexos_articulos_set.exists() else None)
#         if anexos_form.is_valid():
#             anexo = anexos_form.save(commit=False)
#             anexo.IdArticuloFK = articulo
#             anexo.save()
#         return super().form_valid(form)
    

    
class Borrar_ArticulosView(DeleteView):
    model = Articulo
    template_name = 'shared/del.html'

    def get_success_url(self):
        if self.request.accepts('application/json'):
            return JsonResponse({'success': True})  # Cerrar la modal si la solicitud acepta JSON
        else:
            return reverse_lazy('ACTIVOS:Listar_ART')

    def form_valid(self, form):
        articulo = self.get_object()
        log_event(self.request.user,'info', f'Se elimino el Articulo {articulo.Descripcion}')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['title'] = 'Borrar Articulos'
        context['entity'] = 'Articulos'
        context['texto'] = f'¿Desea borrar el Articulo {self.object.Descripcion}?'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_ART')
        return context
    