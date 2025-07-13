from django.db import models
import uuid
from django.conf import settings
from backend.storage_backends import ResourceStorage  # ✅ Importar ResourceStorage


def resource_file_path(instance, filename):
    """Genera un nombre único para evitar sobrescribir archivos."""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"resources/{filename}"


class Resource(models.Model):
    TOOL_CHOICES = [
        ("AgentHub", "AgentHub"),
        ("AgentOps", "AgentOps"),
        ("AutoGPT", "AutoGPT"),
        ("Custom", "Custom"),
        ("Dialogflow", "Dialogflow"),
        ("Flowise", "Flowise"),
        ("Go High Level", "Go High Level"),
        ("LangChain", "LangChain"),
        ("Make", "Make"),
        ("Other", "Other"),
        ("Pipedream", "Pipedream"),
        ("Relevance AI", "Relevance AI"),
        ("Retell AI", "Retell AI"),
        ("Stack AI", "Stack AI"),
        ("TaskMagic", "TaskMagic"),
        ("Tiledesk", "Tiledesk"),
        ("Voiceflow", "Voiceflow"),
        ("Wit.ai", "Wit.ai"),
        ("Zapier", "Zapier"),
        ("n8n", "n8n"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tool = models.CharField(max_length=50, choices=TOOL_CHOICES)
    file = models.FileField(
        upload_to=resource_file_path,
        storage=ResourceStorage(),  # ✅ Asignar ResourceStorage aquí
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
