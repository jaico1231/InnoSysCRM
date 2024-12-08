
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from ActivosFijos.models.articulos import Articulo
from ActivosFijos.models.anexo_articulo import Anexos_Articulos
from ActivosFijos.forms import ArticuloForm, Anexos_ArticuloForm

class Anexos_ArticulosView(TemplateView):
    model = Anexos_Articulos
    template_name = 'Articulos/Detalle_Articulos.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Articulos'
    #     context['entity'] = 'Articulos'
    #     context['list_url'] = reverse_lazy('ACTIVOS:Listar_ART')
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Articulos'
        context['entity'] = 'Articulos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_ART')
        context['articulo_form'] = ArticuloForm()
        context['anexos_form'] = Anexos_ArticuloForm()
        return context

    def post(self, request, *args, **kwargs):
        articulo_form = ArticuloForm(request.POST)
        anexos_form = Anexos_ArticuloForm(request.POST, request.FILES)
        if articulo_form.is_valid() and anexos_form.is_valid():
            articulo = articulo_form.save()
            anexos = anexos_form.save(commit=False)
            anexos.IdArticuloFK = articulo
            anexos.save()
            return redirect('ACTIVOS:Listar_ART')
        else:
            return render(request, self.template_name, {'articulo_form': articulo_form, 'anexos_form': anexos_form})
    # def post (self, request, *args, **kwargs):
    #     Articulo_Form = ArticuloForm(request.POST, request.FILES)
    #     Anexos_Articulos_Form = Anexos_ArticuloForm(request.POST, request.FILES)
    #     if Articulo_Form.is_valid() and Anexos_Articulos_Form.is_valid():
    #         Articulo = Articulo_Form.save()
    #         Anexos_Articulos = Anexos_Articulos_Form.save(commit=False)
    #         Anexos_Articulos.Articulo = Articulo
    #         Anexos_Articulos.save()
    #         return redirect('ACTIVOS:Listar_ART')
    #     else:
    #         return render(request, self.template_name, {'ArticuloForm': Articulo_Form, 'Anexos_ArticulosForm': Anexos_Articulos_Form})



class Crear_Anexos_ArticulosView(CreateView):
    form_class = Anexos_ArticuloForm
    template_name = 'Anexos/Crear_Anexos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_ART')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     Articulo = Articulo.self.get_object()
    #     Anexos_Articulos = Anexos_Articulos.objects.filter(Articulo=Articulo)
    #     context['Anexos_ArticulosForm'] = Anexos_ArticuloForm(instance=Anexos_Articulos)
    #     context['title'] = 'Listar Anexos'
    #     context['entity'] = 'Anexos'
    #     return context
    # def form_valid(self, form):
    #     Articulo = form.save()
    #     Anexos_ArticuloForm = Anexos_ArticuloForm(self.request.POST, self.request.FILES, instance=Anexos_Articulos)
    #     if Anexos_ArticuloForm.is_valid():
    #         Anexos_ArticuloForm.save()
    #     return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Anexos'
        context['entity'] = 'Anexos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_ART')
        return context
    
class Editar_Anexos_ArticulosView(UpdateView):
    model = Anexos_Articulos
    form_class = Anexos_ArticuloForm
    template_name = 'Anexos/Crear_Anexos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_ART')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Anexos'
        context['entity'] = 'Anexos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_ART')
        return context
class Borrar_Anexos_ArticulosView(DeleteView):
    model = Anexos_Articulos
    template_name = 'Anexos/Borrar_Anexos.html'
    success_url = reverse_lazy('ACTIVOS:Listar_Articulos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Anexos'
        context['entity'] = 'Anexos'
        context['list_url'] = reverse_lazy('ACTIVOS:Listar_Articulos')
        return context
