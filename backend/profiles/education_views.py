from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .education_models import Education
from .models import CandidateProfile
from .education_serializers import EducationSerializer


class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return education for the current user's profile."""
        try:
            profile = self.request.user.candidate_profile
            return profile.education.all()
        except CandidateProfile.DoesNotExist:
            return Education.objects.none()

    def perform_create(self, serializer):
        """Associate education with the current user's profile."""
        profile = self.request.user.candidate_profile
        serializer.save(profile=profile)
