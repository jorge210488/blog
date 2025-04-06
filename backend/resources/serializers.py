from rest_framework import serializers
from .models import Resource
from django.core.exceptions import ValidationError


class ResourceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.SerializerMethodField()  # 👈 nuevo campo visible en GET
    file = serializers.FileField(required=False)

    class Meta:
        model = Resource
        fields = [
            "id",
            "title",
            "description",
            "tool",
            "file",
            "user_id",  # 👈 lo agregamos al response
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_user_id(self, obj):
        return str(obj.user_id) if obj.user_id else None

    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("El título no puede estar vacío.")
        return value

    def validate_tool(self, value):
        valid_tools = [choice[0] for choice in Resource.TOOL_CHOICES]
        if value not in valid_tools:
            raise ValidationError(f"La herramienta debe ser una de {valid_tools}.")
        return value

    def validate_file(self, value):
        if value and not value.name.endswith(".json"):
            raise ValidationError("Solo se permiten archivos JSON.")
        return value
