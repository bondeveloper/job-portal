from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import EmployerUser
from .job_models import Job


class JobPublishView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can publish jobs.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            job = Job.objects.get(id=job_id, employer=employer_user.employer)
            job.status = 'published'
            job.save()

            return Response({
                'message': 'Job published successfully.',
                'status': job.status
            }, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Job.DoesNotExist:
            return Response(
                {'error': 'Job not found or does not belong to your employer.'},
                status=status.HTTP_404_NOT_FOUND
            )


class JobCloseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can close jobs.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            job = Job.objects.get(id=job_id, employer=employer_user.employer)
            job.status = 'closed'
            job.save()

            return Response({
                'message': 'Job closed successfully.',
                'status': job.status
            }, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Job.DoesNotExist:
            return Response(
                {'error': 'Job not found or does not belong to your employer.'},
                status=status.HTTP_404_NOT_FOUND
            )


class JobUnpublishView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can unpublish jobs.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            job = Job.objects.get(id=job_id, employer=employer_user.employer)
            job.status = 'draft'
            job.save()

            return Response({
                'message': 'Job unpublished successfully.',
                'status': job.status
            }, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Job.DoesNotExist:
            return Response(
                {'error': 'Job not found or does not belong to your employer.'},
                status=status.HTTP_404_NOT_FOUND
            )


class JobMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            job = Job.objects.get(id=job_id, employer=employer_user.employer)

            return Response({
                'job_id': job.id,
                'title': job.title,
                'status': job.status,
                'applications_count': 0,
                'views_count': 0,
            }, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Job.DoesNotExist:
            return Response(
                {'error': 'Job not found or does not belong to your employer.'},
                status=status.HTTP_404_NOT_FOUND
            )
