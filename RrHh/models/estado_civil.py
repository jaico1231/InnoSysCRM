from django.db import models

# Soltero,
# Casado,
# Divorciado,
# Viudo,
# Union Libre

class estado_civil(models.Model):
    Estado = models.CharField(max_length=15, unique=True)
    def __str__(self):
        return self.Estado
    class Meta:
        verbose_name="estado_civil"
        verbose_name_plural = 'estado_civil'
        ordering = ['Estado']
