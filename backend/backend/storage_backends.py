# backend/storage_backends.py
from storages.backends.s3boto3 import S3Boto3Storage

print("🛠️ Cargando backend.storage_backends.py")


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
