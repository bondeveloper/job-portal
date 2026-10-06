from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CandidateProfile
from .profile_utils import is_profile_complete


class ProfileStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            is_complete = is_profile_complete(profile)
            return Response({
                'profile_id': profile.id,
                'status': profile.status,
                'is_complete': is_complete,
                'message': 'Profile is searchable by employers' if profile.status == 'active' else 'Profile is not yet searchable'
            }, status=status.HTTP_200_OK)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
