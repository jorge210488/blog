from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import User, Credential
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class CredentialSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Credential
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": False,
            },  # Password no obligatorio
            "user": {"required": False},
        }


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    credential = CredentialSerializer()  # Anidamos el serializer

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": False,
            }  # <- Evita exigir password aquí
        }

    def create(self, validated_data):
        """Crea User y Credential en una sola transacción"""
        credential_data = validated_data.pop("credential", None)

        # Crear el usuario
        user = User.objects.create(**validated_data)

        # Crear credenciales si se proporcionan
        if credential_data:
            Credential.objects.create(user=user, **credential_data)

        return user

    def update(self, instance, validated_data):
        credential_data = validated_data.pop("credential", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if credential_data:
            Credential.objects.update_or_create(user=instance, defaults=credential_data)

        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid credentials.")

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        try:
            credential = user.credential
        except Credential.DoesNotExist:
            raise AuthenticationFailed("No credentials found for this user.")

        if not credential.is_verified:
            raise AuthenticationFailed("Account is not verified.")

        if not credential.password or not check_password(password, credential.password):
            raise AuthenticationFailed("Invalid credentials.")

        refresh = RefreshToken.for_user(user)
        refresh["user_id"] = str(user.id)

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
