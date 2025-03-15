from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Resource
from .serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los recursos JSON.
    - Cualquier usuario puede listar los recursos.
    - Solo autenticados pueden subir, modificar o eliminar archivos.
    - Solo autenticados pueden descargar los archivos JSON.
    """

    queryset = Resource.objects.all().order_by("-created_at")
    serializer_class = ResourceSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"  # ✅ Se asegura de usar `id` en lugar de `pk`

    def get_permissions(self):
        """Define permisos personalizados según la acción"""
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]  # Permitir ver la lista de recursos sin autenticación
        return [IsAuthenticated()]  # Solo autenticados pueden modificar o eliminar

    def perform_create(self, serializer):
        """Asigna automáticamente el usuario autenticado al crear un recurso."""
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Solo permite que los usuarios autenticados descarguen el archivo JSON."""
        resource = get_object_or_404(
            Resource, id=kwargs.get("id")
        )  # ✅ Evita errores con `.get("id")`

        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                "Debes estar autenticado para descargar archivos."
            )

        return FileResponse(resource.file.open(), as_attachment=True)
