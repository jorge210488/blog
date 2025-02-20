from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Credential
from .serializers import UserSerializer, CredentialSerializer, LoginSerializer
from rest_framework.views import APIView
from utils.email import send_verification_email
import os
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """🔹 CRUD para User con manejo de Signup"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return User.objects.all()

    def get_permissions(self):
        # Permitir acceso público para crear usuarios
        if self.action == "create":
            return [AllowAny()]
        # Proteger GET y PATCH con autenticación
        elif self.action in ["list", "retrieve", "partial_update", "update"]:
            return [IsAuthenticated()]
        # Otros métodos protegidos por defecto
        return super().get_permissions()

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

        # Construir la URL de verificación directamente desde el backend
        verify_path = f"/api/accounts/credentials/{user.credential.id}/verify/"
        verify_url = self.request.build_absolute_uri(verify_path)

        # Obtener el nombre para el correo
        given_name = user.first_name

        # Llamar a la función que envía el correo
        send_verification_email(
            to_email=user.email,
            given_name=given_name,
            verification_url=verify_url,
            template_id=os.getenv("SENDGRID_TEMPLATE_VERIFICATION_ID"),
        )


class CredentialViewSet(viewsets.ModelViewSet):
    """🔹 CRUD para Credential"""

    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    lookup_field = "id"

    def get_permissions(self):
        # Permitir acceso público al endpoint de verificación
        if self.action == "verify_account":
            return [AllowAny()]
        # Proteger GET y PATCH con autenticación
        elif self.action in ["list", "retrieve", "partial_update", "update"]:
            return [IsAuthenticated()]
        # Otros métodos protegidos por defecto
        return super().get_permissions()

    @action(detail=True, methods=["patch"], url_path="verify")
    def verify_account(self, request, id=None):
        """
        ✅ Verifica la cuenta del usuario (is_verified = True)
        """
        credential = self.get_object()
        if credential.is_verified:
            return Response(
                {"message": "Account is already verified."}, status=status.HTTP_200_OK
            )

        credential.is_verified = True
        credential.save()

        return Response(
            {"message": "Account successfully verified."}, status=status.HTTP_200_OK
        )


class LoginView(APIView):
    """
    🔐 Endpoint para Login de Usuarios.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(
            raise_exception=True
        ):  # Usa raise_exception para mostrar errores
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
