from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import redirect
from .models import User, Credential
from .serializers import (
    UserSerializer,
    CredentialSerializer,
    LoginSerializer,
    AvatarUploadSerializer,
)
from rest_framework.views import APIView
from utils.email import send_verification_email
from rest_framework.permissions import AllowAny, IsAuthenticated
import os
from .permissions import IsAdminUserOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action == "list":
            return [IsAuthenticated(), IsAdminUserOnly()]
        elif self.action in ["retrieve", "partial_update", "update"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_context(self):
        """Pasa el request al serializer para validar permisos en `update`."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = serializer.save()  # Guarda el usuario

        # Construir la URL de verificación
        verify_path = f"/api/accounts/credentials/{user.credential.id}/verify/"
        verify_url = self.request.build_absolute_uri(verify_path)

        # Obtener el nombre para el correo
        given_name = user.first_name

        # Obtener el template_id desde el entorno o definir un valor por defecto
        template_id = os.getenv(
            "SENDGRID_TEMPLATE_VERIFICATION_ID", "default_template_id"
        )

        # Llamar a la función que envía el correo
        send_verification_email(
            to_email=user.email,
            given_name=given_name,
            verification_url=verify_url,
            template_id=template_id,  # ✅ Aquí incluimos el template_id
        )

    @action(detail=True, methods=["post"], url_path="upload-avatar")
    def upload_avatar(self, request, id=None):
        user = self.get_object()
        serializer = AvatarUploadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({"img_url": user.img_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action == "verify_account":
            return [AllowAny()]
        elif self.action in ["list", "retrieve", "partial_update", "update"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(
        detail=True,
        methods=["get", "patch"],
        url_path="verify",
        permission_classes=[AllowAny],
    )
    def verify_account(self, request, id=None):
        credential = self.get_object()

        if credential.is_verified:
            return Response({"message": "Account is already verified."}, status=200)

        credential.is_verified = True
        credential.save()

        # 🔁 Opcional: redirigir a tu frontend
        return redirect("https://d1zdy7m13ps0e9.cloudfront.net/")


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
