from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .certification_models import Certification
from .models import CandidateProfile
from .certification_serializers import CertificationSerializer


class CertificationViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return certifications for the current user's profile."""
        try:
            profile = self.request.user.candidate_profile
            return profile.certifications.all()
        except CandidateProfile.DoesNotExist:
            return Certification.objects.none()

    def perform_create(self, serializer):
        """Associate certification with the current user's profile."""
        profile = self.request.user.candidate_profile
        serializer.save(profile=profile)
