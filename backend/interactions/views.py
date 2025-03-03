from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Like, Bookmark
from .serializers import CommentSerializer, LikeSerializer, BookmarkSerializer

# from accounts.permissions import IsAdminUserOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
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


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
