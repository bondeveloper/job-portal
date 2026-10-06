from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import EmployerUser
from .shortlist_models import CandidateShortlist
from .shortlist_serializers import ShortlistCandidateSerializer, AddToShortlistSerializer
from profiles.models import CandidateProfile


class ShortlistListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            shortlist = CandidateShortlist.objects.filter(employer=employer_user.employer)
            serializer = ShortlistCandidateSerializer(shortlist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can shortlist candidates.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = AddToShortlistSerializer(data=request.data)
            if serializer.is_valid():
                candidate_id = serializer.validated_data['candidate_id']
                candidate = CandidateProfile.objects.get(id=candidate_id)

                if CandidateShortlist.objects.filter(
                    employer=employer_user.employer,
                    candidate=candidate
                ).exists():
                    return Response(
                        {'error': 'Candidate is already shortlisted.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                shortlist = CandidateShortlist.objects.create(
                    employer=employer_user.employer,
                    candidate=candidate
                )

                result_serializer = ShortlistCandidateSerializer(shortlist)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )


class ShortlistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, shortlist_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            shortlist = CandidateShortlist.objects.get(
                id=shortlist_id,
                employer=employer_user.employer
            )
            shortlist.delete()
            return Response({'message': 'Candidate removed from shortlist.'}, status=status.HTTP_204_NO_CONTENT)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except CandidateShortlist.DoesNotExist:
            return Response(
                {'error': 'Shortlist item not found or does not belong to your employer.'},
                status=status.HTTP_404_NOT_FOUND
            )
