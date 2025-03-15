from django.db import models
import uuid
from django.conf import settings


def resource_file_path(instance, filename):
    """Genera un nombre único para evitar sobrescribir archivos."""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"resources/{filename}"


class Resource(models.Model):
    TOOL_CHOICES = [
        ("Relevance AI", "Relevance AI"),
        ("Make", "Make"),
        ("n8n", "n8n"),
        ("Other", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tool = models.CharField(max_length=50, choices=TOOL_CHOICES)
    file = models.FileField(
        upload_to=resource_file_path
    )  # Guardar en /media/resources/
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
