from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsOrgAdmin
from .models import Document
from .serializers import DocumentSerializer



class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(organization=self.request.user.organization)

    def get_permissions(self):
        if self.action in ("list", "retreive"):
            return [IsAuthenticated()]
        return [IsOrgAdmin()]

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.organization,
            uploaded_by=self.request.user,
        )