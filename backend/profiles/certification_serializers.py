from rest_framework import serializers
from .certification_models import Certification


class CertificationSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = ['id', 'name', 'issuer', 'issue_date', 'expiry_date', 'credential_id', 'credential_url', 'is_expired', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_expired', 'created_at', 'updated_at']

    def get_is_expired(self, obj):
        return obj.is_expired
