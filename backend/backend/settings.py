"""
Django settings for backend project.
"""

import os
import pymysql
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from django.core.files.storage import default_storage
from backend.storage_backends import ImageStorage, ResourceStorage, AvatarStorage

pymysql.install_as_MySQLdb()
load_dotenv()

# ✅ Define BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Configuración de AWS S3 para **dos buckets diferentes**
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-east-2")

# ✅ Nombre de los buckets
AWS_IMAGES_BUCKET_NAME = os.getenv("AWS_IMAGES_BUCKET_NAME")  # Bucket para imágenes
AWS_RESOURCES_BUCKET_NAME = os.getenv(
    "AWS_RESOURCES_BUCKET_NAME"
)  # Bucket para resources
AWS_AVATARS_BUCKET_NAME = os.getenv("AWS_AVATARS_BUCKET_NAME")  # Bucket para avatares

# GOOGLE AUTHENTICATION ID
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


# ✅ Configuración avanzada de S3
AWS_QUERYSTRING_AUTH = False  # Permitir acceso a archivos sin firma temporal
AWS_S3_FILE_OVERWRITE = False  # Evita sobrescribir archivos con el mismo nombre
AWS_DEFAULT_ACL = None  # No aplicar ACL por defecto en S3

# ✅ Configurar almacenamiento por tipo de archivo
DEFAULT_FILE_STORAGE = (
    "backend.storage_backends.ImageStorage"  # 🔥 Para imágenes de posts
)
RESOURCE_FILE_STORAGE = (
    "backend.storage_backends.ResourceStorage"  # 🔥 Para archivos en resources
)

# ✅ URLs base de los archivos en S3
MEDIA_URL = (
    f"https://{AWS_IMAGES_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/images/"
)
RESOURCES_URL = f"https://{AWS_RESOURCES_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/resources/"
AVATARS_URL = (
    f"https://{AWS_AVATARS_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/avatars/"
)


# 🔥 🔥 🔥 Se inicializan storages para que no se rompa `ResourceStorage`
default_storage._wrapped = ImageStorage()
resource_storage = ResourceStorage()
avatar_storage = AvatarStorage()

print(
    f"✅ DEFAULT_FILE_STORAGE en tiempo de ejecución: {default_storage.__class__.__name__}"
)
print(
    f"✅ RESOURCE_FILE_STORAGE en tiempo de ejecución: {resource_storage.__class__.__name__}"
)


# ✅ Configuración de seguridad
SECRET_KEY = "django-insecure-+7%k+n()kjkw@hc=q#(%ss1h&&ofplk6!x7rr4nc-k-*p^3)ql"
DEBUG = True

ALLOWED_HOSTS = ["*"]

# ✅ Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "accounts",
    "posts",
    "interactions",
    "resources",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
]

# ✅ Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

# ✅ Configuración de TEMPLATES para Django Admin
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# ✅ Configuración de Base de Datos con MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ✅ Modelo de usuario personalizado
AUTH_USER_MODEL = "accounts.User"

# ✅ Configuración de REST Framework y JWT
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.authentication.UUIDJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

SIMPLE_JWT = {
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# ✅ Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://tu-dominio.com",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]

# ✅ Configuración de archivos estáticos y media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ✅ Configuración de SendGrid para envío de correos
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
