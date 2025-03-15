from rest_framework import serializers
from .models import Resource
from django.core.exceptions import ValidationError


class ResourceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = serializers.FileField(required=True)

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

    def validate_file(self, value):
        """Solo permite archivos JSON."""
        if not value.name.endswith(".json"):
            raise ValidationError("Only JSON files are allowed.")
        return value
