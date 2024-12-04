# geografia.py
from django.db import models

class Paises(models.Model):
    Nombre = models.CharField(max_length=60)
    Iso_name = models.CharField(max_length=50)
    alfa2 = models.CharField(max_length=2)
    alfa3 = models.CharField(max_length=3)
    Codigo = models.CharField(max_length=3)
    gentilicio = models.CharField(max_length=60, blank=True, null=True)
    def __str__ (self):
        return str(self.Nombre)

    class Meta:
        verbose_name="Pais"
        verbose_name_plural = 'Pais'
        ordering = ['Nombre']

class Departamentos(models.Model):
    Departamento = models.CharField(max_length=60)
    Paises = models.ForeignKey(Paises, on_delete=models.CASCADE)
    def __str__ (self):
        return str(self.Departamento)

    class Meta:
        verbose_name="Departamento"
        verbose_name_plural = 'Departamento'
        ordering = ['Departamento']

class Municipios(models.Model):
    Municipio = models.CharField("Municipio", max_length=255, blank=False, null=False)
    Departamentos = models.ForeignKey(Departamentos, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Municipio)
    class Meta:
        verbose_name="Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['Municipio']

class Comuna(models.Model):
    Nombre = models.CharField("Comuna",max_length=100)
    Municipio = models.ForeignKey(Municipios, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre
    class Meta:
         verbose_name = 'Comuna'
         verbose_name_plural = 'Comunas'
         ordering = ['Nombre']

class Barrio(models.Model):
    Nombre = models.CharField("Barrio",max_length=100)
    Comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre
    class Meta:
         verbose_name = 'Barrio'
         verbose_name_plural = 'Barrios'
         ordering = ['Nombre']