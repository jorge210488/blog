from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Credential
from .serializers import UserSerializer, CredentialSerializer, LoginSerializer
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    """🔹 CRUD para User con manejo de Signup"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

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
        serializer.save()


class CredentialViewSet(viewsets.ModelViewSet):
    """🔹 CRUD para Credential"""

    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer

    @action(detail=True, methods=["patch"], url_path="verify")
    def verify_account(self, request, pk=None):
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

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(
            raise_exception=True
        ):  # Usa raise_exception para mostrar errores
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
