# posts/models.py

from django.db import models
import uuid
from django.conf import settings
from backend.storage_backends import ImageStorage


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    tags = models.ManyToManyField("Tag", related_name="posts", blank=True)
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resources = models.ManyToManyField(
        "resources.Resource", related_name="posts", blank=True
    )

    # 🔥 Nuevo campo para la URL del video
    video_url = models.URLField(
        blank=True, null=True, help_text="URL de un video de YouTube o Vimeo"
    )

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        storage=ImageStorage(), upload_to=""
    )  # 🔥 Se subirá a S3 automáticamente
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.post.title}"
