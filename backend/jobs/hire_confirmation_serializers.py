from rest_framework import serializers
from .hire_confirmation_models import HireConfirmation


class HireConfirmationSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='application.job.employer.name', read_only=True)
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    job_location = serializers.CharField(source='application.job.location', read_only=True)
    job_salary_min = serializers.IntegerField(source='application.job.salary_min', read_only=True)
    job_salary_max = serializers.IntegerField(source='application.job.salary_max', read_only=True)

    class Meta:
        model = HireConfirmation
        fields = ['id', 'status', 'employer_name', 'job_title', 'job_location', 'job_salary_min', 'job_salary_max',
                  'employer_confirmed', 'candidate_confirmed', 'employer_confirmed_at', 'candidate_confirmed_at',
                  'hire_finalized_at']
        read_only_fields = ['id', 'status', 'employer_name', 'job_title', 'job_location', 'job_salary_min',
                           'job_salary_max', 'employer_confirmed', 'candidate_confirmed', 'employer_confirmed_at',
                           'candidate_confirmed_at', 'hire_finalized_at']
