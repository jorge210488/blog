# backend/storage_backends.py
from storages.backends.s3boto3 import S3Boto3Storage

print("🛠️ Cargando backend.storage_backends.py")


class ResourceStorage(S3Boto3Storage):
    """Almacenamiento para resources en un bucket específico"""

    bucket_name = "jam-resources-json"
    location = "resources"
    file_overwrite = False


class ImageStorage(S3Boto3Storage):
    """Almacenamiento para imágenes de posts en otro bucket"""

    bucket_name = "jam-blog-images"
    location = "images"
    file_overwrite = False
