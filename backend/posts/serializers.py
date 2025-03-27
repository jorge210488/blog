from rest_framework import serializers
from .models import Category, Tag, Post, PostImage
from resources.serializers import ResourceSerializer


class PostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ["id", "image", "image_url"]  # 🔥 Agrega la URL pública

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url  # 🔥 Retorna la URL de S3 directamente
        return None


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )
    images = PostImageSerializer(
        many=True, read_only=True
    )  # 🔥 Muestra imágenes existentes
    resources = ResourceSerializer(many=True, read_only=True)

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
            "images",
            "resources",
            "views",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["views", "created_at", "updated_at"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        images_data = self.context["request"].FILES.getlist("images")

        # 🔥 Crear post
        post = Post.objects.create(**validated_data)
        post.tags.set(tags_data)

        # 🔥 Asignar recursos (ManyToManyField)
        resources_ids = self.context["request"].data.getlist("resources")
        if resources_ids:
            post.resources.set(resources_ids)

        # 🔥 Validar y subir imágenes
        if len(images_data) > 10:
            raise serializers.ValidationError(
                {"images": "No puedes subir más de 10 imágenes."}
            )

        for image in images_data:
            if image.size > 1024 * 1024:
                raise serializers.ValidationError(
                    {"images": "Cada imagen debe pesar menos de 1MB."}
                )
            PostImage.objects.create(post=post, image=image)

        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        images_data = self.context["request"].FILES.getlist(
            "images"
        )  # 🔥 Nuevas imágenes

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags_data is not None:
            instance.tags.set(tags_data)

        if images_data:
            instance.images.all().delete()  # 🔥 Borra imágenes antiguas antes de agregar nuevas
            if len(images_data) > 10:
                raise serializers.ValidationError(
                    {"images": "No puedes subir más de 10 imágenes."}
                )

            for image in images_data:
                if image.size > 1024 * 1024:
                    raise serializers.ValidationError(
                        {"images": "Cada imagen debe pesar menos de 1MB."}
                    )
                PostImage.objects.create(
                    post=instance, image=image
                )  # 🔥 Se sube automáticamente a S3

        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)  # 🔥 Cantidad de posts
    posts = PostSerializer(many=True, read_only=True)  # 🔥 Lista de posts

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "post_count", "posts"]


class TagSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Tag
        fields = "__all__"


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    author = serializers.StringRelatedField()
    images = PostImageSerializer(
        many=True, read_only=True
    )  # 🔥 Incluye imágenes con sus URLs en S3

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
            "images",
            "views",
            "status",
            "created_at",
            "updated_at",
        ]
