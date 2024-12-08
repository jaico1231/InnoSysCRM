from django.db import models
from shared.models.baseModel import BaseModel
class Estado_Actividad(BaseModel):
    Id_EstadoActividad = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=250, unique=True)
    Observacion = models.CharField(max_length=500, blank=True)
    FechaCreacion = models.DateTimeField('fecha creación', auto_now_add=True )
    
    def __str__(self):
        return self.Descripcion
    class Meta:
        verbose_name="EstadoActividad"
        verbose_name_plural = 'EstadoActividad'
        ordering = ['Descripcion']


#esta tabla contiene el estado de las actividades en proceso, realizados, atrasados
#se usa con el cronograma de mantenimiento o cualquier cronograma