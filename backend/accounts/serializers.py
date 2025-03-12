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
            "password": {"write_only": True, "required": False},
        }

    def validate(self, attrs):
        """
        Se ejecuta antes de `update()` y `create()` para validar restricciones.
        """

        # 🚫 Bloquear intento de modificar `is_superuser`
        if "is_superuser" in attrs:
            raise serializers.ValidationError(
                {"is_superuser": "You are not allowed to modify this field."}
            )

        return attrs

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
        """
        Permite actualizar User y Credential, con restricciones en `role`, `is_staff` y `is_superuser`.
        """
        request = self.context["request"]
        credential_data = validated_data.pop("credential", None)

        # 🚫 Bloquear cambio de `is_superuser`
        if "is_superuser" in validated_data:
            raise serializers.ValidationError(
                {"is_superuser": "You are not allowed to modify this field."}
            )

        # 🚫 Solo `is_superuser` puede cambiar `is_staff`
        if "is_staff" in validated_data:
            if not request.user.is_superuser:
                raise serializers.ValidationError(
                    {"is_staff": "Only superusers can modify this field."}
                )

        # 🚫 Solo `is_superuser` o `is_staff` pueden cambiar `role`
        if "role" in validated_data:
            if not (request.user.is_superuser or request.user.is_staff):
                raise serializers.ValidationError(
                    {"role": "Only staff or superusers can modify this field."}
                )

        # Actualizar usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Si hay datos de Credential, actualizarlos
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
        refresh["email"] = user.email
        refresh["role"] = user.role

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }
