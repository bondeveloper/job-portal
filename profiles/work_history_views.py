from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CandidateProfile
from .work_history_models import WorkHistory
from .work_history_serializers import WorkHistorySerializer


class WorkHistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            work_history = WorkHistory.objects.filter(profile=profile).order_by('-start_date')
            serializer = WorkHistorySerializer(work_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            if profile.user != request.user:
                return Response({'error': 'You can only update your own profile'}, status=status.HTTP_403_FORBIDDEN)

            serializer = WorkHistorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(profile=profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class WorkHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, work_history_id):
        try:
            work_history = WorkHistory.objects.get(id=work_history_id, profile__pk=pk)
            serializer = WorkHistorySerializer(work_history)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WorkHistory.DoesNotExist:
            return Response({'error': 'Work history not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk, work_history_id):
        try:
            work_history = WorkHistory.objects.get(id=work_history_id, profile__pk=pk)
            if work_history.profile.user != request.user:
                return Response({'error': 'You can only update your own profile'}, status=status.HTTP_403_FORBIDDEN)

            serializer = WorkHistorySerializer(work_history, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WorkHistory.DoesNotExist:
            return Response({'error': 'Work history not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, work_history_id):
        try:
            work_history = WorkHistory.objects.get(id=work_history_id, profile__pk=pk)
            if work_history.profile.user != request.user:
                return Response({'error': 'You can only update your own profile'}, status=status.HTTP_403_FORBIDDEN)

            work_history.delete()
            return Response({'message': 'Work history deleted'}, status=status.HTTP_204_NO_CONTENT)
        except WorkHistory.DoesNotExist:
            return Response({'error': 'Work history not found'}, status=status.HTTP_404_NOT_FOUND)
