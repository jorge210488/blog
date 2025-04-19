from utils.email import send_contact_email
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class ContactView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        subject = data.get("subject")
        message = data.get("message")
        alt_email = data.get("alt_email")
        phone = data.get("phone")

        user = request.user if request.user and request.user.is_authenticated else None

        if not user:
            return Response({"detail": "Authentication required."}, status=401)

        send_contact_email(
            subject=subject,
            user_email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            message=message,
            alt_email=alt_email,
            phone=phone,
        )

        return Response({"message": "Mensaje enviado correctamente."}, status=200)
