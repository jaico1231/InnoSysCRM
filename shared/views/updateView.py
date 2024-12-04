import csv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib import messages
from django.apps import apps

class CargarCSVView(View):
    template_name = 'shared/upload.html'
    success_message = "Datos cargados con éxito"
    model_name = None  # El modelo será dinámico

    def post(self, request):
        # Verificar si el archivo CSV está en los datos de la solicitud
        if 'csv_file' not in request.FILES:
            messages.error(request, "Por favor seleccione un archivo CSV.")
            return redirect(reverse_lazy('shared:index'))

        csv_file = request.FILES['csv_file']

        try:
            # Intentar decodificar el archivo CSV
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            # Obtener el modelo dinámicamente
            model = apps.get_model(app_label='shared', model_name=self.model_name)
            if not model:
                messages.error(request, f"Modelo no encontrado: {self.model_name}")
                return JsonResponse({'success': False, 'error': 'Modelo no encontrado'}, status=400)

            # Insertar los datos en el modelo
            for row in reader:
                if row:  # Verificar que la fila no esté vacía
                    try:
                        # Mostrar el contenido de la fila a cargar
                        print(f"Datos de la fila: {row}")
                        model.objects.create(**row)
                    except Exception as e:
                        messages.error(request, f"Error al crear objeto: {str(e)}")

            messages.success(request, self.success_message)
            return redirect(reverse_lazy('shared:index'))

        except csv.Error as e:
            messages.error(request, f"Error al leer el archivo CSV: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")

        return redirect(reverse_lazy('shared:index'))

    def get_context_data(self, **kwargs):
        context = {
            'title': 'Cargar datos desde CSV',
        }
        return context

    def get(self, request):
        context = self.get_context_data()  # Ahora esto funcionará
        return render(request, self.template_name, context)

class ConfirmCSVUploadView(View):
    def get(self, request, *args, **kwargs):
        # Obtener los datos del CSV desde la sesión
        csv_data = request.session.get('csv_data', None)
        return render(request, 'shared/confirm_upload.html', {'csv_data': csv_data})

    def post(self, request, *args, **kwargs):
        # Obtener datos del CSV
        csv_data = request.POST.get('csv_data')

        # Guardar los datos en la sesión para poder acceder a ellos en la vista de confirmación
        request.session['csv_data'] = csv_data

        # Procesar los datos del CSV
        success = self.procesar_datos_csv(csv_data)

        if success:
            messages.success(request, 'Datos cargados exitosamente.')
            return JsonResponse({'success': True, 'message': 'Datos procesados y guardados.'})
        else:
            messages.error(request, 'Error al procesar los datos.')
            return JsonResponse({'success': False, 'message': 'Error al procesar los datos.'})

    def procesar_datos_csv(self, csv_data):
        # Aquí puedes implementar la lógica para procesar y guardar los datos en la base de datos
        try:
            # Supongamos que csv_data es un string con datos CSV
            decoded_data = csv_data.splitlines()
            reader = csv.DictReader(decoded_data)

            # Obtener el modelo dinámicamente (ajusta según tu lógica)
            model = apps.get_model(app_label='shared', model_name='Terceros')  # Cambia 'Terceros' según sea necesario

            for row in reader:
                if row:  # Verificar que la fila no esté vacía
                    # Filtrar los campos problemáticos
                    filtered_row = self.filtrar_campos(row)
                    if filtered_row:  # Verificar que la fila filtrada no esté vacía
                        try:
                            model.objects.create(**filtered_row)  # Guardar el objeto en la base de datos
                        except Exception as e:
                            print(f"Error al crear objeto con datos {filtered_row}: {str(e)}")
                            # Puedes registrar el error o manejarlo como desees

            return True  # Retornar True si todo fue exitoso
        except Exception as e:
            print(f"Error al procesar datos: {str(e)}")
            return False  # Retornar False si hubo un error

    def filtrar_campos(self, row):
        # Lista de campos a omitir que generan errores
        campos_a_omitir = ['user_created', 'created_at', 'user_updated', 'updated_at', 'TipoDocumento', 'Estado', 'pais', 'departamento', 'municipio', 'update_img', 'Tipo_Tercero', 'asesor']  # Añade otros campos problemáticos aquí
        # Crear un nuevo diccionario sin los campos problemáticos
        return {key: value for key, value in row.items() if key not in campos_a_omitir}
        
# class ConfirmCSVUploadView(View):
# #ver que datos estoy recibiendo aqui
#     def get(self, request, *args, **kwargs):
#         return render(request, 'shared/confirm_upload.html')
    
#     def post(self, request, *args, **kwargs):
#         # Aquí procesarías los datos del CSV recibidos en la solicitud
#         csv_data = request.POST.get('csv_data')  # Obtener datos del CSV

#         # Aquí podrías agregar la lógica para procesar los datos del CSV

#         return JsonResponse({'success': True})  # Retornar una respuesta JSON
    

def generar_csv_modelo(request, app_label, model_name):
    try:
        model = apps.get_model(app_label=app_label, model_name=model_name)
         
    except LookupError:
        return HttpResponse("Modelo no encontrado", status=404)
    
    campos_excluidos = {'id','user_created', 'created_at', 'user_updated', 'updated_at', 'TipoDocumento', 'Estado', 'pais', 'departamento', 'municipio', 'update_img', 'Tipo_Tercero', 'asesor'}

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}_template.csv"'

    writer = csv.writer(response)
    field_names = [field.name for field in model._meta.fields if field.name not in campos_excluidos]
    writer.writerow(field_names)

    return response

