from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import EmployerUser
from jobs.application_models import JobApplication
from jobs.hire_confirmation_models import HireConfirmation
from jobs.hire_confirmation_serializers import HireConfirmationSerializer


class MarkApplicationHiredView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, application_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can mark applications as hired.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            application = JobApplication.objects.get(
                id=application_id,
                job__employer=employer_user.employer
            )

            if application.status == 'rejected':
                return Response(
                    {'error': 'Cannot hire a rejected application.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            hire_confirmation, created = HireConfirmation.objects.get_or_create(
                application=application,
                defaults={
                    'employer_confirmed': True,
                    'employer_confirmed_at': timezone.now(),
                    'status': 'pending_candidate'
                }
            )

            if not created:
                if hire_confirmation.status in ['confirmed', 'declined']:
                    return Response(
                        {'error': f'Cannot re-mark hired. Current status: {hire_confirmation.status}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = HireConfirmationSerializer(hire_confirmation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except JobApplication.DoesNotExist:
            return Response(
                {'error': 'Application not found or does not belong to your employer.'},
                status=status.HTTP_404_NOT_FOUND
            )
