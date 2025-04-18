# accounts/views_google.py

from rest_framework.views import APIView
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import User, Credential
from rest_framework_simplejwt.tokens import RefreshToken
import os


class GoogleAuthView(APIView):
    permission_classes = []

    def post(self, request):
        id_token_str = request.data.get("token")
        print("📥 Token recibido en request.data:", id_token_str)

        if not id_token_str:
            print("❌ No se recibió token")
            return Response({"detail": "Token is required."}, status=400)

        try:
            print(
                "🔍 Verificando token con GOOGLE_CLIENT_ID:",
                os.getenv("GOOGLE_CLIENT_ID"),
            )

            idinfo = id_token.verify_oauth2_token(
                id_token_str, requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
            )

            print("✅ Token verificado. Info:", idinfo)

            email = idinfo["email"]
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")
            picture = idinfo.get("picture", "")

            print("👤 Usuario:", email, first_name, last_name)

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "img_url": picture,
                    "role": "author",
                },
            )

            print("🆕 Usuario creado?", created)

            Credential.objects.update_or_create(
                user=user,
                defaults={
                    "auth_provider": "google",
                    "is_verified": True,
                },
            )

            refresh = RefreshToken.for_user(user)
            refresh["user_id"] = str(user.id)
            refresh["email"] = user.email
            refresh["role"] = user.role

            print("🎫 Tokens generados correctamente")

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "img_url": user.img_url,
                    },
                }
            )

        except ValueError as e:
            print("❌ Error al verificar token:", str(e))
            return Response({"detail": "Invalid token", "error": str(e)}, status=400)
