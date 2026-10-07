from rest_framework import serializers
from .document_models import SupportingDocument


class SupportingDocumentSerializer(serializers.ModelSerializer):
    file_size_kb = serializers.SerializerMethodField()

    class Meta:
        model = SupportingDocument
        fields = ['id', 'document_type', 'file', 'file_name', 'file_size', 'file_size_kb', 'created_at']
        read_only_fields = ['id', 'file_size', 'file_name', 'created_at']

    def get_file_size_kb(self, obj):
        return obj.file_size / 1024 if obj.file_size else 0
