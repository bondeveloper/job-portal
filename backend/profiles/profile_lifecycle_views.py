from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CandidateProfile


class ProfilePauseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            if profile.user != request.user:
                return Response({'error': 'You can only manage your own profile'}, status=status.HTTP_403_FORBIDDEN)

            if profile.status == 'archived':
                return Response({'error': 'Cannot pause an archived profile'}, status=status.HTTP_400_BAD_REQUEST)

            if profile.status == 'paused':
                return Response({'error': 'Profile is already paused'}, status=status.HTTP_400_BAD_REQUEST)

            profile.status = 'paused'
            profile.save(update_fields=['status', 'updated_at'])
            return Response({
                'message': 'Profile paused successfully',
                'status': profile.status
            }, status=status.HTTP_200_OK)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class ProfileUnpauseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            if profile.user != request.user:
                return Response({'error': 'You can only manage your own profile'}, status=status.HTTP_403_FORBIDDEN)

            if profile.status == 'archived':
                return Response({'error': 'Cannot unpause an archived profile'}, status=status.HTTP_400_BAD_REQUEST)

            if profile.status != 'paused':
                return Response({'error': 'Profile is not paused'}, status=status.HTTP_400_BAD_REQUEST)

            profile.status = 'active'
            profile.save(update_fields=['status', 'updated_at'])
            return Response({
                'message': 'Profile unpaused successfully',
                'status': profile.status
            }, status=status.HTTP_200_OK)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class ProfileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            if profile.user != request.user:
                return Response({'error': 'You can only manage your own profile'}, status=status.HTTP_403_FORBIDDEN)

            if profile.status == 'archived':
                return Response({'error': 'Profile is already archived'}, status=status.HTTP_400_BAD_REQUEST)

            profile.status = 'archived'
            profile.save(update_fields=['status', 'updated_at'])
            return Response({
                'message': 'Profile deleted (archived). Data will be permanently deleted after 90 days.',
                'status': profile.status
            }, status=status.HTTP_200_OK)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
