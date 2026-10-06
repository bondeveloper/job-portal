from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CandidateProfile
from .skill_models import Skill, CandidateSkill
from .skill_serializers import CandidateSkillSerializer, SkillSerializer


class SkillListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CandidateSkillView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            skills = CandidateSkill.objects.filter(profile=profile).select_related('skill')
            skill_data = [{'id': cs.skill.id, 'name': cs.skill.name} for cs in skills]
            return Response(skill_data, status=status.HTTP_200_OK)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            profile = CandidateProfile.objects.get(pk=pk)
            if profile.user != request.user:
                return Response({'error': 'You can only update your own profile'}, status=status.HTTP_403_FORBIDDEN)

            serializer = CandidateSkillSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(profile)
                skills = CandidateSkill.objects.filter(profile=profile).select_related('skill')
                skill_data = [{'id': cs.skill.id, 'name': cs.skill.name} for cs in skills]
                return Response(skill_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
