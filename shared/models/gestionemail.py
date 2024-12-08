from django.db import models
from shared.models.baseModel import BaseModel

class EstadoEmail(BaseModel):
    estado = models.CharField(max_length=50)
    sigla = models.CharField(max_length=2)
    
    def __str__(self):
        return self.estado
class Email(BaseModel):
    subject = models.CharField(max_length=255)
    body_text = models.TextField()
    body_html = models.TextField(blank=True, null=True)
    from_email = models.EmailField()
    to_email = models.EmailField()
    attachment_path = models.CharField(max_length=255, blank=True, null=True)
    status = models.ForeignKey(EstadoEmail, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id