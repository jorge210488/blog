from rest_framework import serializers
from .models import Resource
from django.core.exceptions import ValidationError


class ResourceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = serializers.FileField(required=False)  # ✅ Ahora es opcional en `update`

    class Meta:
        model = Resource
        fields = [
            "id",
            "title",
            "description",
            "tool",
            "file",
            "user",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_title(self, value):
        """Verifica que el título no esté vacío."""
        if not value.strip():
            raise ValidationError("El título no puede estar vacío.")
        return value

    def validate_tool(self, value):
        """Verifica que la herramienta seleccionada sea válida."""
        valid_tools = [choice[0] for choice in Resource.TOOL_CHOICES]
        if value not in valid_tools:
            raise ValidationError(f"La herramienta debe ser una de {valid_tools}.")
        return value

    def validate_file(self, value):
        """Solo permite archivos JSON."""
        if value and not value.name.endswith(".json"):
            raise ValidationError("Solo se permiten archivos JSON.")
        return value
