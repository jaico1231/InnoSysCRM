from django.views.generic import View

# class Detalle_Contratos(DetailView):
#     model = Contrato_Laboral
#     template_name = 'cartas/Contrato_Laboral.html'
#     iniciales = Empresa.objects.get(id=1)


        
#     def post(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['iniciales'] = self.iniciales
#         contrato = self.get_object()
#         salario_texto = number_to_words(int(contrato.salario)).upper()  # Convertir salario a texto
#         # fecha_texto = date_to_words(contrato.fecha_inicio(yyyy, mm, dd))  # Convertir fecha de inicio a texto

#         dia_en_letras = num2words(contrato.fecha_inicio.day, lang='es').capitalize()
#         html = template.render(context)
#         response = HttpResponse(content_type='application/pdf')
#         pisa_status = pisa.CreatePDF(html, dest=response)

#         if pisa_status.err:
#             return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
#         # Convierte el mes a letras
#         mes_en_letras = contrato.fecha_inicio.strftime('%B')
#         if mes_en_letras == 'January':
#             mes_en_letras = 'Enero'
#         elif mes_en_letras == 'February':
#             mes_en_letras = 'Febrero'
#         elif mes_en_letras == 'March':
#             mes_en_letras = 'Marzo'
#         elif mes_en_letras == 'April':
#             mes_en_letras = 'Abril'
#         elif mes_en_letras == 'May':
#             mes_en_letras = 'Mayo'
#         elif mes_en_letras == 'June':
#             mes_en_letras = 'Junio'
#         elif mes_en_letras == 'July':
#             mes_en_letras = 'Julio'
#         elif mes_en_letras == 'August':
#             mes_en_letras = 'Agosto'
#         elif mes_en_letras == 'September':
#             mes_en_letras = 'Septiembre'
#         elif mes_en_letras == 'October':
#             mes_en_letras = 'Octubre'
#         elif mes_en_letras == 'November':
#             mes_en_letras = 'Noviembre'
#         elif mes_en_letras == 'December':
#             mes_en_letras = 'Diciembre'  
        
#         # Convierte el año a letras
#         anio_en_letras = num2words(contrato.fecha_inicio.year, lang='es').capitalize()
#         print (contrato.fecha_inicio)
        
#         context['salario_texto'] = salario_texto
#         context['dia_en_letras'] = dia_en_letras
#         context['mes_en_letras'] = mes_en_letras
#         context['anio_en_letras'] = anio_en_letras
#         context['title'] = 'Contratos'
#         context['entity'] = 'Contratos'
#         context['list_url'] = reverse_lazy('RrHh:Listar_Contratos')
#         return context
