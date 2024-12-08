from django.db import models
    # ("CC", "Cedula de Ciudadania"), 
    # ("CE", "Cedula de Extranjería"),
    # ("PT", "Pasaporte"),
    # ("TI", "Tarjeta de Identidad"),
    # ("CD", "Carnet Diplomatico"),
    # ("NIT", "Numero de Identificacion Tributaria"),
    # ("RC", "Registro Civil"),
class Tipo_Documento(models.Model):
    Sigla = models.CharField(max_length=5)
    Descripcion = models.CharField(max_length=100)

    def __str__ (self):
        return f'{self.Sigla} - {self.Descripcion}'
    class Meta:
        verbose_name="tipodoc"
        verbose_name_plural = 'tipodoc'
        ordering = ['Descripcion']