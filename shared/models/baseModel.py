from django.db import models
from django.conf import settings
class BaseModel(models.Model):
    user_created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_user_created',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_user_updated',null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        abstract = True