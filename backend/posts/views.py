from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Category, Tag, Post
from .serializers import (
    CategorySerializer,
    TagSerializer,
    PostSerializer,
    PostDetailSerializer,
)
from accounts.permissions import IsAdminUserOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUserOnly()]


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
    queryset = Post.objects.all()
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PostDetailSerializer  # Para vistas de lectura más detalladas
        return PostSerializer  # Para crear/actualizar posts

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario autenticado como autor
        serializer.save(author=self.request.user)
