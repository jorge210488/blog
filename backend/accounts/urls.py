from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CredentialViewSet, LoginView

# 🔥 Creamos el router para registrar las rutas automáticamente
router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"credentials", CredentialViewSet)

urlpatterns = [
    path("", include(router.urls)),  # ✅ Incluye todas las rutas del router
    path("login/", LoginView.as_view(), name="login"),
]
