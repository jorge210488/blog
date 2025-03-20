from django.db.models import Count
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Tag, Post
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
    queryset = Post.objects.all().order_by("-created_at")
    lookup_field = "id"

    permission_classes = [AllowAny]

    # ✅ Agregamos filtros
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = [
        "category__slug"
    ]  # Permite filtrar por categoría usando el `slug`
    search_fields = ["title", "content"]  # Permite buscar por título y contenido
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PostDetailSerializer  # Para vistas de lectura más detalladas
        return PostSerializer  # Para crear/actualizar posts

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
