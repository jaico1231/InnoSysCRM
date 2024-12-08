from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from Comercial.forms.cotizacionForm import *
from django.forms import inlineformset_factory

class CrearCotizacionView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('Comercial.add_cotizacion',)
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizaciones/crear_cotizacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DetalleCotizacionFormSet = inlineformset_factory(Cotizacion, DetalleCotizacion, form=DetalleCotizacionForm, extra=1)

        if self.request.POST:
            context['formset'] = DetalleCotizacionFormSet(self.request.POST)
            context['nuevo_producto_form'] = NuevoProductoForm(self.request.POST)
        else:
            context['formset'] = DetalleCotizacionFormSet()
            context['nuevo_producto_form'] = NuevoProductoForm()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        nuevo_producto_form = context['nuevo_producto_form']

        if formset.is_valid() and nuevo_producto_form.is_valid():
            self.object = form.save()

            if nuevo_producto_form.cleaned_data.get('nombre'):
                nuevo_producto = nuevo_producto_form.save()
                DetalleCotizacion.objects.create(
                    cotizacion=self.object,
                    producto=nuevo_producto,
                    cantidad=nuevo_producto_form.cleaned_data.get('cantidad', 1),
                    precio_unitario=nuevo_producto_form.cleaned_data.get('precio', 0),
                )

            formset.instance = self.object
            formset.save()
            return redirect('cotizaciones:detalle', pk=self.object.pk)
        else:
            return self.form_invalid(form)

class EditarCotizacionView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('Comercial.change_cotizacion',)
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizaciones/crear_cotizacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DetalleCotizacionFormSet = inlineformset_factory(Cotizacion, DetalleCotizacion, form=DetalleCotizacionForm, extra=1)

        if self.request.POST:
            context['formset'] = DetalleCotizacionFormSet(self.request.POST, instance=self.object)
            context['nuevo_producto_form'] = NuevoProductoForm(self.request.POST)
        else:
            context['formset'] = DetalleCotizacionFormSet(instance=self.object)
            context['nuevo_producto_form'] = NuevoProductoForm()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        nuevo_producto_form = context['nuevo_producto_form']

        if formset.is_valid() and nuevo_producto_form.is_valid():
            self.object = form.save()

            if nuevo_producto_form.cleaned_data.get('nombre'):
                nuevo_producto = nuevo_producto_form.save()
                DetalleCotizacion.objects.create(
                    cotizacion=self.object,
                    producto=nuevo_producto,
                    cantidad=nuevo_producto_form.cleaned_data.get('cantidad', 1),
                    precio_unitario=nuevo_producto_form.cleaned_data.get('precio', 0),
                )

            formset.instance = self.object
            formset.save()
            return redirect('cotizaciones:detalle', pk=self.object.pk)
        else:
            return self.form_invalid(form)