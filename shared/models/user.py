import re
from django.db import models
from django.contrib.auth.models import  AbstractUser, GroupManager, Group
from shared.models.tipo_documento import Tipo_Documento

def Cargar_imagenes_articulos_path(instance, filename):
    # Obtener el número de documento del tercero
    identificacion = instance.NumeroIdentificacion
    # Reemplazar espacios en blanco por guiones bajos y eliminar caracteres especiales
    identificacion = re.sub(r'\W+', '_', str(identificacion))
    # Obtener la extensión del archivo
    ext = filename.split('.')[-1]
    # Devolver la ruta de subida del archivo
    return f'img/profile/{identificacion}/{filename}'

class User(AbstractUser):
    TipoDocumento = models.ForeignKey(Tipo_Documento, on_delete=models.CASCADE, blank=True, null=True)
    NumeroIdentificacion = models.CharField( max_length=50,null=True, blank=True, unique=True)
    image = models.ImageField(upload_to=Cargar_imagenes_articulos_path, verbose_name='Imagen de perfil', blank=True, null=True)

    # Evitar conflictos en relaciones inversas
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Personaliza el related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Personaliza el related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'img/profile/user-1.jpg'

    def __str__(self):
        return f"{self.NumeroIdentificacion} {self.first_name} {self.last_name}"