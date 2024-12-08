
from django.db import models

from shared.models.baseModel import BaseModel
    # "Administrador",
    # "Analista de sistemas",
    # "Programador",
    # "Disenador",
    # "Desarrollador",
    # "Operario de producción",
    # "Contador",
    # "Gerente",
    # "Jefe de RrHh",
    # "Jefe de Compras",
    # "Asistente",
    # "Auxiliar",
    # "Secretaria",
class Cargo(BaseModel):
    cargo = models.CharField(max_length=100)
    def __str__(self):
        return self.cargo
    class Meta:
        verbose_name="cargo"
        verbose_name_plural = 'cargo'
        ordering = ['cargo']