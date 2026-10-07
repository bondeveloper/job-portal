from rest_framework import viewsets, status, parsers, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .document_models import SupportingDocument
from .models import CandidateProfile
from .document_serializers import SupportingDocumentSerializer


class SupportingDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = SupportingDocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def get_queryset(self):
        """Only return documents for the current user's profile."""
        try:
            profile = self.request.user.candidate_profile
            return profile.supporting_documents.all()
        except CandidateProfile.DoesNotExist:
            return SupportingDocument.objects.none()

    def perform_create(self, serializer):
        """Associate document with the current user's profile."""
        profile = self.request.user.candidate_profile

        # Check max documents limit (5)
        if profile.supporting_documents.count() >= 5:
            raise serializers.ValidationError("Maximum 5 supporting documents allowed.")
        
        serializer.save(profile=profile)

    def perform_destroy(self, instance):
        """Delete supporting document and cleanup file."""
        instance.file.delete(save=False)
        instance.delete()
