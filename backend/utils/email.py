import os
import requests
import json


def send_verification_email(to_email, given_name, verification_url, template_id):
    """
    📧 Envía un correo de verificación usando SendGrid directamente con requests.
    - Usa `verify=False` si DEBUG=True, para evitar errores SSL en desarrollo.
    """
    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {
        "Authorization": f"Bearer {os.getenv('SENDGRID_API_KEY')}",
        "Content-Type": "application/json",
    }

    data = {
        "from": {"email": os.getenv("DEFAULT_FROM_EMAIL")},
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "dynamic_template_data": {
                    "given_name": given_name,
                    "verification_link": verification_url,
                },
            }
        ],
        "template_id": template_id,
    }

    try:
        is_dev = os.getenv("DEBUG", "False").lower() == "true"

        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            verify=not is_dev,  # ❗ Solo en local ignora SSL
        )

        print(f"✅ SendGrid response: {response.status_code} - {response.text}")
        return response.status_code

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return None


def send_contact_email(
    subject, user_email, first_name, last_name, message, alt_email=None, phone=None
):
    """
    ✉️ Envía un correo simple desde el formulario de contacto
    """
    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {
        "Authorization": f"Bearer {os.getenv('SENDGRID_API_KEY')}",
        "Content-Type": "application/json",
    }

    from_email = os.getenv("DEFAULT_FROM_EMAIL")
    to_email = "jorgemartinez.jam@gmail.com"

    full_name = f"{first_name} {last_name}"

    body = f"""
📩 Nuevo mensaje desde el formulario de contacto:

👤 Nombre: {full_name}
📧 Correo principal: {user_email}
📭 Correo alternativo: {alt_email or "No proporcionado"}
📱 Teléfono: {phone or "No proporcionado"}

📝 Mensaje:
{message}
    """

    data = {
        "from": {"email": from_email},
        "personalizations": [{"to": [{"email": to_email}]}],
        "subject": subject,
        "content": [{"type": "text/plain", "value": body.strip()}],
    }

    try:
        is_dev = os.getenv("DEBUG", "False").lower() == "true"

        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            verify=not is_dev,
        )

        print(f"📬 Contact email response: {response.status_code} - {response.text}")
        return response.status_code

    except Exception as e:
        print(f"❌ Error sending contact email: {e}")
        return None
