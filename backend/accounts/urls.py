from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CredentialViewSet, LoginView

# 🔥 Creamos el router para registrar las rutas automáticamente
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"credentials", CredentialViewSet, basename="credential")

# urls.py
urlpatterns = [
    path("", include(router.urls)),
    path(
        "users/<uuid:pk>/",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="user-detail",
    ),  # Add this line
    path("login/", LoginView.as_view(), name="login"),
]
