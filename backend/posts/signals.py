# posts/signals.py
import os
import json
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from posts.models import Category, Tag


@receiver(post_migrate)
def preload_categories_and_tags(sender, **kwargs):
    base_path = os.path.join(settings.BASE_DIR, "posts", "fixtures")

    # ✅ CATEGORÍAS
    categories_path = os.path.join(base_path, "categories.json")
    if os.path.exists(categories_path):
        with open(categories_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for entry in data:
                fields = entry["fields"]
                name = fields["name"]
                slug = fields["slug"]
                if not Category.objects.filter(name=name, slug=slug).exists():
                    Category.objects.create(**fields)
                    print(f"🟢 Categoría creada: {name}")
                else:
                    print(f"🟡 Categoría ya existe: {name}")

    # ✅ TAGS
    tags_path = os.path.join(base_path, "tags.json")
    if os.path.exists(tags_path):
        with open(tags_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for entry in data:
                fields = entry["fields"]
                name = fields["name"]
                slug = fields["slug"]
                if not Tag.objects.filter(name=name, slug=slug).exists():
                    Tag.objects.create(**fields)
                    print(f"🟢 Tag creado: {name}")
                else:
                    print(f"🟡 Tag ya existe: {name}")
