import os

from rest_framework import serializers

from .models import Document

ALLOWED_EXTENSIONS = {".txt", ".pdf"}
MAX_SIZE = 5 * 1024 * 1024  # 5 MB


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "title", "file", "status", "error", "created_at")
        read_only_fields = ("id", "status", "error", "created_at")

    def validate_file(self, f):
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError("Only .txt and .pdf files are allowed.")
        if f.size > MAX_SIZE:
            raise serializers.ValidationError("File too large (max 5 MB).")
        return f