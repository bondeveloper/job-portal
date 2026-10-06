from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from .models import EmployerUser
from profiles.models import CandidateProfile
from profiles.skill_models import CandidateSkill
from profiles.availability_models import Availability


class CandidateSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter', 'viewer']:
                return Response(
                    {'error': 'Only employer users can search candidates.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            queryset = CandidateProfile.objects.filter(status='active').select_related('user').prefetch_related('skills', 'availability')

            location = request.query_params.get('location', '')
            if location:
                queryset = queryset.filter(location__icontains=location)

            skills = request.query_params.getlist('skills')
            if skills:
                try:
                    skill_ids = [int(s) for s in skills]
                    queryset = queryset.filter(skills__id__in=skill_ids).distinct()
                except (ValueError, TypeError):
                    pass

            salary_min = request.query_params.get('salary_min')
            if salary_min:
                try:
                    salary_min = int(salary_min)
                    queryset = queryset.filter(
                        availability__salary_max__gte=salary_min
                    )
                except (ValueError, TypeError):
                    pass

            salary_max = request.query_params.get('salary_max')
            if salary_max:
                try:
                    salary_max = int(salary_max)
                    queryset = queryset.filter(
                        availability__salary_min__lte=salary_max
                    )
                except (ValueError, TypeError):
                    pass

            employment_type = request.query_params.get('employment_type', '')
            if employment_type:
                queryset = queryset.filter(availability__employment_type=employment_type)

            sort = request.query_params.get('sort', '-created_at')
            if sort in ['-created_at', 'created_at']:
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
            profiles = queryset[start:end]

            results = []
            for profile in profiles:
                skills_list = [{'id': skill.id, 'name': skill.name} for skill in profile.skills.all()]
                availability = profile.availability if hasattr(profile, 'availability') else None
                results.append({
                    'id': profile.id,
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'location': profile.location,
                    'phone': profile.phone,
                    'skills': skills_list,
                    'availability': {
                        'employment_type': availability.employment_type if availability else None,
                        'salary_min': availability.salary_min if availability else None,
                        'salary_max': availability.salary_max if availability else None,
                    } if availability else None,
                    'created_at': profile.created_at
                })

            return Response({
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'results': results
            }, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
