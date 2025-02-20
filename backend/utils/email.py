import os
import certifi
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import urllib3


def send_verification_email(to_email, given_name, verification_url, template_id):
    """
    📧 Envía un correo de verificación usando SendGrid.
    """
    message = Mail(
        from_email=os.getenv("DEFAULT_FROM_EMAIL"),
        to_emails=to_email,
    )

    # Agregar el template y datos dinámicos
    message.template_id = template_id
    message.dynamic_template_data = {
        "given_name": given_name,
        "verification_link": verification_url,
    }

    try:
        # Crear un PoolManager con el certificado de certifi
        http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

        # Usar SendGrid API Client sin pasar directamente http (usa requests internamente)
        sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code

    except Exception as e:
        print(f"Error sending email: {e}")
        return None
