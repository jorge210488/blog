from django.db.models import Count
from rest_framework import viewsets, filters, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Tag, Post, PostImage
from .serializers import (
    CategorySerializer,
    TagSerializer,
    PostSerializer,
    PostDetailSerializer,
)
from accounts.permissions import IsAdminUserOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(post_count=Count("posts")).prefetch_related(
        "posts"
    )  # 🔥 Agrega `post_count`
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    # ✅ Agregar filtros (Opcional: permite filtrar por slug)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["slug"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUserOnly()]


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.select_related("category", "author")
        .prefetch_related("tags", "images", "resources")
        .order_by("-created_at")
    )
    lookup_field = "id"
    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["category__slug", "status", "author_id", "tags__id"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PostDetailSerializer  # 🔥 Serializador detallado para lectura
        return PostSerializer  # 🔥 Serializador normal para escritura

    def perform_create(self, serializer):
        """Maneja la creación del post, incluyendo imágenes y recursos en S3"""
        post = serializer.save(author=self.request.user)

        # 🔹 Obtener imágenes desde la request
        images_data = self.request.FILES.getlist("images")
        if len(images_data) > 10:
            raise serializers.ValidationError(
                {"images": "No puedes subir más de 10 imágenes."}
            )

        for image in images_data:
            if image.size > 1024 * 1024:  # 1MB en bytes
                raise serializers.ValidationError(
                    {"images": "Cada imagen debe pesar menos de 1MB."}
                )
            PostImage.objects.create(
                post=post, image=image
            )  # 🔥 Sube a S3 automáticamente

        return post
