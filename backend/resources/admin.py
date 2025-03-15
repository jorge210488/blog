from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "tool", "created_at")
    search_fields = ("title", "user__username", "tool")
    list_filter = ("tool", "created_at")
