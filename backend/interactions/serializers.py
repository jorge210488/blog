from rest_framework import serializers
from .models import Comment, Like, Bookmark


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)  # 👈 este muestra el email
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user",  # ahora sí será visible y mostrará el email
            "content",
            "parent_comment",
            "replies",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True, context=self.context).data


class LikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # Autoasigna el usuario autenticado

    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["created_at"]


class BookmarkSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # Autoasigna el usuario autenticado

    class Meta:
        model = Bookmark
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["created_at"]
