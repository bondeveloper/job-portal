from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from profiles.models import CandidateProfile
from .application_models import JobApplication
from .hire_confirmation_models import HireConfirmation
from .hire_confirmation_serializers import HireConfirmationSerializer


class HireStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        try:
            candidate_profile = CandidateProfile.objects.get(user=request.user)
            application = JobApplication.objects.get(id=application_id, candidate=candidate_profile)

            try:
                hire_confirmation = HireConfirmation.objects.get(application=application)
                serializer = HireConfirmationSerializer(hire_confirmation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except HireConfirmation.DoesNotExist:
                return Response(
                    {'error': 'No hire offer for this application yet.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except CandidateProfile.DoesNotExist:
            return Response(
                {'error': 'Candidate profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except JobApplication.DoesNotExist:
            return Response(
                {'error': 'Application not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class AcceptHireView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, application_id):
        try:
            candidate_profile = CandidateProfile.objects.get(user=request.user)
            application = JobApplication.objects.get(id=application_id, candidate=candidate_profile)

            try:
                hire_confirmation = HireConfirmation.objects.get(application=application)

                if hire_confirmation.candidate_confirmed:
                    return Response(
                        {'error': 'You have already accepted this hire offer.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                hire_confirmation.candidate_confirmed = True
                hire_confirmation.candidate_confirmed_at = timezone.now()
                hire_confirmation.status = 'confirmed'
                hire_confirmation.hire_finalized_at = timezone.now()
                hire_confirmation.save()

                application.status = 'hired'
                application.hired_at = timezone.now()
                application.save()

                serializer = HireConfirmationSerializer(hire_confirmation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except HireConfirmation.DoesNotExist:
                return Response(
                    {'error': 'No hire offer for this application.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except CandidateProfile.DoesNotExist:
            return Response(
                {'error': 'Candidate profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except JobApplication.DoesNotExist:
            return Response(
                {'error': 'Application not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class DeclineHireView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, application_id):
        try:
            candidate_profile = CandidateProfile.objects.get(user=request.user)
            application = JobApplication.objects.get(id=application_id, candidate=candidate_profile)

            try:
                hire_confirmation = HireConfirmation.objects.get(application=application)

                if hire_confirmation.status == 'declined':
                    return Response(
                        {'error': 'You have already declined this hire offer.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                hire_confirmation.candidate_confirmed = False
                hire_confirmation.candidate_confirmed_at = timezone.now()
                hire_confirmation.status = 'declined'
                hire_confirmation.save()

                application.status = 'rejected'
                application.save()

                serializer = HireConfirmationSerializer(hire_confirmation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except HireConfirmation.DoesNotExist:
                return Response(
                    {'error': 'No hire offer for this application.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except CandidateProfile.DoesNotExist:
            return Response(
                {'error': 'Candidate profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except JobApplication.DoesNotExist:
            return Response(
                {'error': 'Application not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
