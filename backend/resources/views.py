from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Resource
from .serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los recursos JSON.
    - Cualquier usuario puede listar todos los recursos.
    - Solo autenticados pueden subir, modificar o eliminar archivos.
    - Solo autenticados pueden descargar los archivos JSON.
    - Endpoint `/api/resources/user/` devuelve los recursos del usuario autenticado.
    - Endpoint `/api/resources/{id}/download/` descarga el archivo de un recurso (protegido).
    """

    queryset = Resource.objects.all().order_by("-updated_at")
    serializer_class = ResourceSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "description"]
    filterset_fields = ["tool"]
    ordering_fields = ["updated_at"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def download(self, request, id=None):
        """
        🔐 Descarga protegida del archivo del recurso.
        URL: `/api/resources/{id}/download/`
        """
        resource = get_object_or_404(Resource, id=id)
        return FileResponse(resource.file.open(), as_attachment=True)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def user(self, request):
        """
        👤 Devuelve solo los recursos del usuario autenticado.
        URL: `/api/resources/user/`
        """
        user_resources = Resource.objects.filter(user=request.user).order_by(
            "-updated_at"
        )
        serializer = self.get_serializer(user_resources, many=True)
        return Response(serializer.data)
