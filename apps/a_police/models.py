from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import os
# Create your models here.
# TODO-Documentación
User = get_user_model()

def user_document_path(instance, filename):
    """Genera la ruta donde se guardará el archivo"""
    return f'documents/user_{instance.user.id}/type_{instance.type}/{filename}'

class Document(models.Model):
    types = [
        (1,  "Acta de nacimiento"),
        (2,  "Curriculum"),
        (3,  "CURP"),
        (4,  "RFC"),
        (5,  "IMSS"),
        (6,  "INE"),
        (7,  "Licencia de manejo"),
        (8,  "Cartilla de servicio militar"),
        (9,  "Certificado de estudios"),
        (10, "Comprobante de domicilio"),
        (11, "Fotografia de frente"),
    ]
    UTILITY_TYPE_CHOICES = [
        ('si', 'si'),
        ('no', 'no'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    type = models.PositiveSmallIntegerField(verbose_name="Nombre del documento",choices=types)
    document = models.FileField(verbose_name="Documento", upload_to=user_document_path ,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Solo archivos PDF menores a 5MB')
    original_name = models.CharField(max_length=255)
    utility_type = models.CharField(
        max_length=20,
        choices=UTILITY_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text='Sabe manejar vehículo'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        unique_together = ['user', 'type']  # Un usuario solo puede tener un documento por tipo
        ordering = ['type']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_type_display()}"
    
    def delete(self, *args, **kwargs):
        """Eliminar archivo del sistema cuando se elimina el registro"""
        if self.document:
            if os.path.isfile(self.document.path):
                os.remove(self.document.path)
        super().delete(*args, **kwargs)