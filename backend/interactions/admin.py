from django.contrib import admin
from .models import Comment, Like, Bookmark


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "content", "created_at")
    search_fields = ("user__username", "post__title", "content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__username", "post__title")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__username", "post__title")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
