
from django.db import models

# A+,
# A-,
# B+,
# B-,
# AB+,
# AB-,
# O+,
# O-
class Grupo_Sanguineo(models.Model):
    grupo = models.CharField(max_length=4,unique=True)
    def __str__(self):
        return self.grupo
    class Meta:
        verbose_name="GrupoSanguineo"
        verbose_name_plural = 'GrupoSanguineo'
        ordering = ['grupo']
