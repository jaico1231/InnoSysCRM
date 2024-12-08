from django.db import models
from ActivosFijos.models.articulos import Articulo
from ActivosFijos.models.presupuestos import Presupuestos
from shared.models.baseModel import BaseModel
from shared.models.terceros import Terceros
from shared.models.user import User
from shared.models.estado import Estado


class OrdenServicio (BaseModel):
    IdOrdenServicio= models.AutoField( primary_key=True ,verbose_name='ID')    
    Tercero =    models.ForeignKey(Terceros, on_delete=models.CASCADE, blank=True, null=True, related_name='IdTerceroFK')
    # este campo es para explicar el motivo de la orden de servicio
    Observaciones= models.TextField(blank=True, null=True)
    FechaRegistro = models.DateTimeField('Fecha Registro',auto_now_add=True)
    FechaAutorizacion = models.DateTimeField('Fecha Ingreso',blank=True, null=True)
    Solicitante = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='Solicitante')
    CreadoPor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='CreadoPor')
    Presupuestos=models.ForeignKey(Presupuestos, on_delete=models.CASCADE, blank=True, null=True, related_name='Presupuestos')#relacion con el presupuesto()
    #el cargo se relaciona desde la consulta
    Costo = models.DecimalField(max_digits=40,blank=True, decimal_places=3,  null=True)
    Autorizado_Por = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='Autorizado_Por')
    Estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default=1)
    Observaciones_adicionales = models.CharField( 'Observaciones', max_length=500, blank=True, null=True)
    prueba = models.CharField( 'Observaciones', max_length=500, blank=True, null=True)
    

    #Metodo para obtener el usuario que genera la orden 
    
    def __str__(self):
        return str(self.IdOrdenServicio)
    class meta:
        verbose_name ="OrdenServicio"
        verbose_name_plural = 'OrdenServicio'
        ordering = ['IdOrdenServicio']



class Articulos_OrdenServicio(BaseModel):
    IdArticulo_OS = models.AutoField ( primary_key=True)
    Orden_servicio =   models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, blank=True, null=True, related_name='IdOrdenServicioFK')
    Articulo =   models.ForeignKey(Articulo, on_delete=models.CASCADE, blank=True, null=True, related_name='IdArticuloFK')
    Cantidad = models.IntegerField(blank=True,  null=True)
    Costo = models.DecimalField(max_digits=40,blank=True, decimal_places=3,  null=True)

    def __str__(self):
        return str(self.IdArticulo_OS)
    
    class meta:
        verbose_name ="Artuculos_OrdenServicio"
        verbose_name_plural = 'Artuculos_OrdenServicio'
        ordering = ['IdArticulo_OS']
