from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q
from employers.job_models import Job
from profiles.skill_models import Skill
from .serializers import JobSearchSerializer


class JobSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Job.objects.filter(status='published').prefetch_related('required_skills__skill', 'employer')

        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        location = request.query_params.get('location', '')
        if location:
            queryset = queryset.filter(location__icontains=location)

        salary_min = request.query_params.get('salary_min')
        if salary_min:
            try:
                salary_min = int(salary_min)
                queryset = queryset.filter(salary_max__gte=salary_min)
            except (ValueError, TypeError):
                pass

        salary_max = request.query_params.get('salary_max')
        if salary_max:
            try:
                salary_max = int(salary_max)
                queryset = queryset.filter(salary_min__lte=salary_max)
            except (ValueError, TypeError):
                pass

        skills = request.query_params.getlist('skills')
        if skills:
            try:
                skill_ids = [int(s) for s in skills]
                queryset = queryset.filter(required_skills__skill__id__in=skill_ids).distinct()
            except (ValueError, TypeError):
                pass

        sort = request.query_params.get('sort', '-created_at')
        if sort in ['-created_at', 'created_at', '-salary_max', 'salary_min']:
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
        jobs = queryset[start:end]

        serializer = JobSearchSerializer(jobs, many=True)
        return Response({
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        }, status=status.HTTP_200_OK)
