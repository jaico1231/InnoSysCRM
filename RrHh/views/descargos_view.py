import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from RrHh.models.llamado_atencion import Descargos, Cuestionario_Descargos, Llamado_Atencion
from RrHh.forms.llamado_atencion_form import Cuestionario_DescargosForm, DescargosForm
from RrHh.views.llamado_atencion import Editar_Llamado_Atencion
from django.forms import inlineformset_factory
now = datetime.datetime.now()


class Listar_Descargos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'RrHh.view_descargos'
    model = Descargos
    template_name = 'descargos/Listar_Descargos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listar Descargos'
        context['entity'] = 'Descargos'
        return context
    
class Crear_Descargos(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'RrHh.add_descargos'
    form_class = DescargosForm
    template_name = 'descargos/crear_descargos.html'
    def get_success_url(self):
        return reverse_lazy('RrHh:Cuestionario_Descargos', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        llamado = Llamado_Atencion.objects.get(pk=self.kwargs['pk'])
        context['Llamado_Atencion'] = llamado
        context['title'] = 'Crear Descargos'
        context['entity'] = 'Descargos'
        context['list_url'] = reverse_lazy('RrHh:Listar_Llamados_Atencion')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_Llamados_Atencion')
        return context

    def form_valid(self, form):
        form.instance.Llamado_Atencion = Llamado_Atencion.objects.get(pk=self.kwargs['pk'])
        form.instance.fecha_descargo = now
        form.instance.user_created = self.request.user
        return super().form_valid(form)

   
class Prueba_Preguntas_Descargos(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'RrHh.add_cuestionario_descargos'
    form_class = Cuestionario_Descargos
    template_name = 'preguntas/cuestionario.html'
    # success_url = reverse_lazy('RrHh:Listar_Llamados_Atencion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Descargos = Descargos.objects.get(pk=self.kwargs['pk'])
        # context['Descargos'] = Descargos
        context['title'] = 'Crear Cuestionario de Descargos'
        context['entity'] = 'Cuestionario de Descargos'
        context['list_url'] = reverse_lazy('RrHh:Listar_Llamados_Atencion')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_Llamados_Atencion')
        return context

    def form_valid(self, form):

        return super().form_valid(form)
    
class Preguntas_Descargos(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'RrHh.add_cuestionario_descargos'
    form_class = Cuestionario_DescargosForm
    template_name = 'preguntas/cuestionario.html'
    success_url = reverse_lazy('RrHh:Listar_Llamados_Atencion')
    def form_valid(self, form):
        form.instance.Descargos_FK = Descargos.objects.get(pk=self.kwargs['pk'])
        form.instance.user_created = self.request.user
        form.save()  # Save the main form

        preguntas = self.request.POST.getlist('preguntas')
        print(preguntas)
        respuestas = self.request.POST.getlist('respuestas')
        print(respuestas)
        anexos = self.request.FILES.getlist('anexos')

        for i in range(len(preguntas)):
            cuestionario = Cuestionario_Descargos(
                Descargos_FK=form.instance.Descargos_FK,
                preguntas=preguntas[i],
                respuestas=respuestas[i],
                anexos=anexos[i] if i < len(anexos) else None,  # Handle cases where there may be fewer files
                user_created=form.instance.user_created
            )
            cuestionario.save()  # Save each question-answer pair

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datos_descargos = Descargos.objects.get(pk=self.kwargs['pk'])
        context['Datos_descargos'] = datos_descargos
        context['title'] = 'Crear Cuestionario de Descargos'
        context['entity'] = 'Cuestionario de Descargos'
        context['list_url'] = reverse_lazy('RrHh:Listar_Llamados_Atencion')
        context['cancel_url'] = reverse_lazy('RrHh:Listar_Llamados_Atencion')
        return context
    

    
#   var form = document.getElementById("myForm");
#   var datos = [];
#   for (var i = 0; i < rowCount; i++) {
#     var pregunta = form.elements["preguntas_" + i].value;
#     var respuesta = form.elements["respuestas_" + i].value;
#     datos.push([pregunta, respuesta]);
#   }
#   alert((datos));


#  function addRow() {
#   var table = document.getElementById("myTable");
#   var row = table.insertRow(-1);
#   var cell1 = row.insertCell(0);
#   var cell2 = row.insertCell(1);
#   cell1.innerHTML = '<textarea name="preguntas" cols="40" rows="3" maxlength="300" id="id_preguntas"></textarea>';
#   cell2.innerHTML = '<textarea name="respuestas" cols="40" rows="3" maxlength="300" id="id_respuestas"></textarea>';
#   var form = document.getElementById("myForm");
#    var datos = [];
#    for (var i = 0; i < rowCount; i++) {
#      var pregunta = form.cell1["preguntas_" + i].value;
#      var respuesta = form.cell1["respuestas_" + i].value;
#      datos.push([pregunta, respuesta]);
#    }
#    alert((datos));
# }  print(self.request.POST.get('nombre_GF'))