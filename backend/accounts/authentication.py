from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

User = get_user_model()


class UUIDJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        print("🔑 Validated Token:", validated_token)

        user_id = validated_token.get("user_id")
        print("🆔 User ID from Token:", user_id)

        if not user_id:
            raise InvalidToken("Token missing 'user_id' claim.")

        # Verificamos que el ID del usuario exista
        try:
            user = User.objects.get(id=user_id)
            print("👤 Found User:", user)
        except User.DoesNotExist:
            print("❌ User not found for ID:", user_id)
            raise AuthenticationFailed("User not found.", code="user_not_found")

        # Verificamos que el usuario esté activo
        if not user.is_active:
            raise AuthenticationFailed("User is inactive.", code="user_inactive")

        return user
