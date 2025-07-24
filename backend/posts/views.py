from django.db.models import Count, Q
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Tag, Post
from .serializers import (
    CategorySerializer,
    TagSerializer,
    PostSerializer,
    PostDetailSerializer,
    PostListSerializer,
)
from accounts.permissions import IsAdminUserOnly
from django.shortcuts import get_object_or_404


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(
        post_count=Count("posts", filter=Q(posts__status="published"))
    ).prefetch_related("posts")
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
        if self.action in ["list", "retrieve", "get_by_slug"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer  # 🔍 Solo para el detalle individual
        elif self.action == "list":
            return PostListSerializer  # ✅ Nueva clase para lista
        return PostSerializer  # Para create/update

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"], url_path="by-slug/(?P<slug>[^/.]+)")
    def get_by_slug(self, request, slug=None):
        post = get_object_or_404(
            Post.objects.select_related("category", "author").prefetch_related(
                "tags", "images", "resources"
            ),
            slug=slug,
        )
        serializer = PostDetailSerializer(post, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def view(self, request, id=None):
        post = self.get_object()
        post.views += 1
        post.save()
        return Response({"views": post.views}, status=status.HTTP_200_OK)
