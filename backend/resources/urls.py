from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet

router = DefaultRouter()
router.register(r"resources", ResourceViewSet, basename="resource")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "resources/user/",
        ResourceViewSet.as_view({"get": "user"}),
        name="user-resources",
    ),  # ✅ Nueva ruta
]
