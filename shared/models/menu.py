# models.py

from django.db import models
from django.contrib.auth.models import Group
from shared.models.baseModel import BaseModel

class Menu(BaseModel):
    name = models.CharField(max_length=100)
    group = models.ManyToManyField(Group, related_name='menu', blank=True)
    estado = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItem(BaseModel):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url_name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    estado = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='menu_items', blank=True)

    def __str__(self):
        return self.name
