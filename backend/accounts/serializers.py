from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Credential
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}, "user": {"required": False}}


class UserSerializer(serializers.ModelSerializer):
    credential = CredentialSerializer()  # 🔹 Anidamos el serializer

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        """Crea User y Credential en una sola transacción"""
        credential_data = validated_data.pop("credential", None)

        # 🔥 Crea el usuario y guarda explícitamente
        user = User.objects.create(**validated_data)

        if credential_data:
            Credential.objects.create(user=user, **credential_data)

        return user

    def update(self, instance, validated_data):
        """Actualiza User y Credential correctamente"""
        credential_data = validated_data.pop("credential", None)

        # Actualiza los campos de User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualiza o crea credenciales
        if credential_data:
            Credential.objects.update_or_create(user=instance, defaults=credential_data)

        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # ✅ Verificar que el usuario exista
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid credentials, please try again.")

        # ✅ Verificar que el usuario esté activo
        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        # ✅ Obtener las credenciales asociadas
        try:
            credential = user.credential
        except Credential.DoesNotExist:
            raise AuthenticationFailed("No credentials found for this user.")

        # ✅ Verificar si el usuario está verificado
        if not credential.is_verified:
            raise AuthenticationFailed(
                "Account is not verified. Please verify your email before signing in."
            )

        # ✅ Verificar la contraseña usando check_password
        if not credential.password or not check_password(password, credential.password):
            raise AuthenticationFailed("Invalid credentials, please try again.")

        # ✅ Generar el token JWT
        refresh = RefreshToken.for_user(user)

        # Retornar datos en validated_data
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            },
        }
