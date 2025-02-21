from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CredentialViewSet, LoginView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"credentials", CredentialViewSet, basename="credential")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
]
