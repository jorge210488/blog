from django.apps import AppConfig
from django.core.management import call_command
from django.db.utils import OperationalError
import os


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"

    def ready(self):
        # Previene que se ejecute dos veces en runserver
        if os.environ.get("RUN_MAIN") != "true":
            return

        try:
            from posts.models import Category, Tag

            if not Category.objects.exists():
                print("🟡 Precargando categorías...")
                call_command("loaddata", "categories.json")

            if not Tag.objects.exists():
                print("🟡 Precargando tags...")
                call_command("loaddata", "tags.json")

        except OperationalError:
            print("⚠️ La base de datos aún no está disponible.")
        except Exception as e:
            print(f"❌ Error al precargar fixtures: {e}")
