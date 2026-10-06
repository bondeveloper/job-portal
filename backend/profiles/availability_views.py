from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CandidateProfile
from .availability_models import Availability
from .availability_serializers import AvailabilitySerializer


class AvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            try:
                availability = Availability.objects.get(profile=profile)
                serializer = AvailabilitySerializer(availability)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Availability.DoesNotExist:
                return Response({'error': 'Availability not set'}, status=status.HTTP_404_NOT_FOUND)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            if profile.user != request.user:
                return Response({'error': 'You can only update your own profile'}, status=status.HTTP_403_FORBIDDEN)

            serializer = AvailabilitySerializer(data=request.data)
            if serializer.is_valid():
                availability, created = Availability.objects.update_or_create(
                    profile=profile,
                    defaults=serializer.validated_data
                )
                return Response(AvailabilitySerializer(availability).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            if profile.user != request.user:
                return Response({'error': 'You can only update your own profile'}, status=status.HTTP_403_FORBIDDEN)

            try:
                availability = Availability.objects.get(profile=profile)
            except Availability.DoesNotExist:
                return Response({'error': 'Availability not set'}, status=status.HTTP_404_NOT_FOUND)

            serializer = AvailabilitySerializer(availability, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
