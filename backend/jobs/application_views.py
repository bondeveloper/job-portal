from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError
from .application_models import JobApplication
from .application_serializers import JobApplicationSerializer, SubmitApplicationSerializer
from employers.job_models import Job
from profiles.models import CandidateProfile


class ApplyToJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        try:
            candidate_profile = CandidateProfile.objects.get(user=request.user)
        except CandidateProfile.DoesNotExist:
            return Response(
                {'error': 'Candidate profile not found. Please complete your profile first.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            job = Job.objects.get(id=job_id, status='published')
        except Job.DoesNotExist:
            return Response(
                {'error': 'Job not found or is not published.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubmitApplicationSerializer(data=request.data)
        if serializer.is_valid():
            cover_letter = serializer.validated_data.get('cover_letter', '')

            try:
                application = JobApplication.objects.create(
                    candidate=candidate_profile,
                    job=job,
                    cover_letter=cover_letter
                )
                result_serializer = JobApplicationSerializer(application)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'error': 'You have already applied to this job.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyApplicationsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            candidate_profile = CandidateProfile.objects.get(user=request.user)
        except CandidateProfile.DoesNotExist:
            return Response(
                {'error': 'Candidate profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        queryset = JobApplication.objects.filter(candidate=candidate_profile).select_related('job', 'job__employer')

        status_filter = request.query_params.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        job_title = request.query_params.get('job_title', '')
        if job_title:
            queryset = queryset.filter(job__title__icontains=job_title)

        sort = request.query_params.get('sort', '-created_at')
        if sort in ['-created_at', 'created_at', 'status']:
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

        serializer = JobApplicationSerializer(applications, many=True)
        return Response({
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        }, status=status.HTTP_200_OK)


class MyApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        try:
            candidate_profile = CandidateProfile.objects.get(user=request.user)
            application = JobApplication.objects.get(id=application_id, candidate=candidate_profile)
            serializer = JobApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
