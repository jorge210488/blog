from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
