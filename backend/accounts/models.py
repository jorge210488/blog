from django.db import models
import uuid
from django.contrib.auth.hashers import make_password


AUTH_PROVIDERS = [
    ("email", "Email"),
    ("google", "Google"),
    ("github", "GitHub"),
    ("linkedin", "LinkedIn"),
]


# ✅ Define a function to generate UUID
def generate_uuid():
    return uuid.uuid4().hex


class User(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
        unique=True,
        default=generate_uuid,
    )  # ✅ Fixed
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[("admin", "Admin"), ("author", "Author")],
        default="author",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Credential(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
        unique=True,
        default=generate_uuid,
    )  # ✅ Fixed
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="credential"
    )
    auth_provider = models.CharField(
        max_length=50, choices=AUTH_PROVIDERS, default="email"
    )
    password = models.CharField(max_length=255, blank=True, null=True)
    auth_token = models.CharField(max_length=500, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.auth_provider == "email" and self.password:
            if not self.password.startswith("pbkdf2_"):
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.auth_provider}"
