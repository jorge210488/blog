from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Comment, Like, Bookmark
from .serializers import CommentSerializer, LikeSerializer, BookmarkSerializer

# from accounts.permissions import IsAdminUserOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Permite lectura pública, pero exige autenticación para escribir
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )  # Asigna automáticamente el usuario autenticado


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # 🔥 Nuevo endpoint: obtener likes por post
    @action(detail=False, methods=["get"], url_path="by-post/(?P<post_id>[^/.]+)")
    def by_post(self, request, post_id=None):
        likes = Like.objects.filter(post_id=post_id)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
