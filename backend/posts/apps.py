from django.apps import AppConfig
from django.db.utils import OperationalError
from django.conf import settings
import os
import json


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return

        try:
            from posts.models import Category, Tag

            base_path = os.path.join(settings.BASE_DIR, "posts", "fixtures")

            # CATEGORÍAS
            categories_path = os.path.join(base_path, "categories.json")
            with open(categories_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for entry in data:
                    fields = entry["fields"]
                    slug = fields["slug"]
                    if not Category.objects.filter(slug=slug).exists():
                        Category.objects.create(**fields)
                        print(f"🟢 Categoría creada: {fields['name']}")

            # TAGS
            tags_path = os.path.join(base_path, "tags.json")
            with open(tags_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for entry in data:
                    fields = entry["fields"]
                    name = fields["name"]
                    if not Tag.objects.filter(name=name).exists():
                        Tag.objects.create(**fields)
                        print(f"🟢 Tag creado: {fields['name']}")

        except OperationalError:
            print("⚠️ La base de datos aún no está disponible.")
        except Exception as e:
            print(f"❌ Error al precargar fixtures: {e}")
