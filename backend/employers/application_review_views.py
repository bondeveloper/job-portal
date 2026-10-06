from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import EmployerUser
from jobs.application_models import JobApplication
from .application_review_models import ApplicationReview
from .application_review_serializers import (
    ApplicationReviewListSerializer,
    ApplicationReviewDetailSerializer,
    ReviewApplicationSerializer
)


class EmployerApplicationsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can view applications.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            queryset = JobApplication.objects.filter(
                job__employer=employer_user.employer
            ).select_related('candidate', 'job', 'job__employer')

            status_filter = request.query_params.get('status', '')
            if status_filter:
                queryset = queryset.filter(status=status_filter)

            job_id = request.query_params.get('job_id')
            if job_id:
                try:
                    job_id = int(job_id)
                    queryset = queryset.filter(job__id=job_id)
                except (ValueError, TypeError):
                    pass

            sort = request.query_params.get('sort', '-created_at')
            if sort in ['-created_at', 'created_at', 'job__title']:
                queryset = queryset.order_by(sort)

            page = request.query_params.get('page', 1)
            try:
                page = int(page)
                if page < 1:
                    page = 1
            except (ValueError, TypeError):
                page = 1

            page_size = 20
            start = (page - 1) * page_size
            end = start + page_size

            total_count = queryset.count()
            applications = queryset[start:end]

            serializer = ApplicationReviewListSerializer(applications, many=True)
            return Response({
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'results': serializer.data
            }, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )


class EmployerApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can view applications.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            application = JobApplication.objects.get(
                id=application_id,
                job__employer=employer_user.employer
            )

            rejection_reason = None
            if hasattr(application, 'review') and application.review:
                rejection_reason = application.review.rejection_reason

            serializer = ApplicationReviewDetailSerializer(application)
            data = serializer.data
            data['rejection_reason'] = rejection_reason
            return Response(data, status=status.HTTP_200_OK)
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

    def patch(self, request, application_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can review applications.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            application = JobApplication.objects.get(
                id=application_id,
                job__employer=employer_user.employer
            )

            serializer = ReviewApplicationSerializer(data=request.data)
            if serializer.is_valid():
                new_status = serializer.validated_data['status']
                rejection_reason = serializer.validated_data.get('rejection_reason', '')

                application.status = new_status
                if new_status == 'rejected':
                    application.updated_at = timezone.now()
                    application.reviewed_at = timezone.now()
                    application.save()
                    ApplicationReview.objects.update_or_create(
                        application=application,
                        defaults={'rejection_reason': rejection_reason}
                    )
                elif new_status == 'reviewed':
                    application.reviewed_at = timezone.now()
                    application.save()

                result_serializer = ApplicationReviewDetailSerializer(application)
                return Response(result_serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
