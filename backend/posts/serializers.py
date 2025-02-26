from rest_framework import serializers
from .models import Category, Tag, Post


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # Asignar el autor automáticamente
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "category",
            "author",
            "tags",
            "image",
            "views",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["views", "created_at", "updated_at"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags_data)
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags_data is not None:
            instance.tags.set(tags_data)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Tag
        fields = "__all__"


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    author = serializers.StringRelatedField()  # Muestra el nombre o email del autor

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "category",
            "author",
            "tags",
            "image",
            "views",
            "status",
            "created_at",
            "updated_at",
        ]
