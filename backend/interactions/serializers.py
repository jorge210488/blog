from rest_framework import serializers
from .models import Comment, Like, Bookmark


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    replies = serializers.SerializerMethodField(read_only=True)  # 🔥

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user",
            "content",
            "parent_comment",
            "replies",  # 👈 incluimos las replies solo nivel 1
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_replies(self, obj):
        # 🔥 Solo retorna los hijos directos (no replies de replies)
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
