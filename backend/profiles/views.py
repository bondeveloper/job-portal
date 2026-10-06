from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CandidateProfile
from .serializers import CandidateProfileSerializer


class CandidateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CandidateProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            serializer = CandidateProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            if profile.user != request.user:
                return Response({'error': 'You can only update your own profile'}, status=status.HTTP_403_FORBIDDEN)
            serializer = CandidateProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                profile = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
