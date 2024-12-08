
from django.db import models

from shared.models.baseModel import BaseModel
class EPS(BaseModel):
    EPS = models.CharField(max_length=100)
    def __str__(self):
        return self.EPS
    class Meta:
        verbose_name="EPS"
        verbose_name_plural = 'EPS'
        ordering = ['EPS']