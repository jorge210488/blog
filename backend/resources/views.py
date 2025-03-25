from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Resource
from .serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los recursos JSON.
    - Cualquier usuario puede listar todos los recursos (método list).
    - Solo autenticados pueden subir, modificar o eliminar archivos.
    - Solo autenticados pueden descargar los archivos JSON.
    - Nuevo endpoint: `/api/resources/user/` para obtener solo los recursos del usuario autenticado.
    """

    queryset = Resource.objects.all().order_by(
        "-updated_at"
    )  # ✅ Ordena por updated_at
    serializer_class = ResourceSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    # Agregar filtros de búsqueda, filtrado y ordenación
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Buscar por `title` y `description`
    search_fields = ["title", "description"]

    # Filtrar por `tool`
    filterset_fields = ["tool"]

    # Ordenar por `updated_at`
    ordering_fields = ["updated_at"]
    ordering = ["-updated_at"]  # ✅ Orden predeterminado (últimos actualizados primero)

    def get_permissions(self):
        """Define permisos personalizados según la acción"""
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Asigna automáticamente el usuario autenticado al crear un recurso."""
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Solo permite que los usuarios autenticados descarguen el archivo JSON."""
        resource = get_object_or_404(Resource, id=kwargs.get("id"))

        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                "Debes estar autenticado para descargar archivos."
            )

        return FileResponse(resource.file.open(), as_attachment=True)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def user(self, request):
        """
        🔹 Endpoint adicional: Obtiene solo los recursos del usuario autenticado.
        URL: `/api/resources/user/`
        """
        user_resources = Resource.objects.filter(user=request.user).order_by(
            "-updated_at"
        )
        serializer = self.get_serializer(user_resources, many=True)
        return Response(serializer.data)
