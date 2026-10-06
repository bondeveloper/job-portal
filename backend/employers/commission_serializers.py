from rest_framework import serializers
from .commission_models import Commission


class CommissionListSerializer(serializers.ModelSerializer):
    candidate_first_name = serializers.CharField(source='hire_confirmation.application.candidate.first_name', read_only=True)
    candidate_last_name = serializers.CharField(source='hire_confirmation.application.candidate.last_name', read_only=True)
    job_title = serializers.CharField(source='hire_confirmation.application.job.title', read_only=True)
    salary_min = serializers.IntegerField(source='hire_confirmation.application.job.salary_min', read_only=True)
    employer_name = serializers.CharField(source='employer.name', read_only=True)

    class Meta:
        model = Commission
        fields = ['id', 'candidate_first_name', 'candidate_last_name', 'job_title', 'salary_min',
                  'employer_name', 'amount', 'rate', 'status', 'created_at', 'invoiced_at', 'paid_at']
        read_only_fields = ['id', 'candidate_first_name', 'candidate_last_name', 'job_title', 'salary_min',
                           'employer_name', 'amount', 'rate', 'created_at', 'invoiced_at', 'paid_at']


class CommissionDetailSerializer(serializers.ModelSerializer):
    candidate_first_name = serializers.CharField(source='hire_confirmation.application.candidate.first_name', read_only=True)
    candidate_last_name = serializers.CharField(source='hire_confirmation.application.candidate.last_name', read_only=True)
    candidate_email = serializers.CharField(source='hire_confirmation.application.candidate.user.email', read_only=True)
    job_title = serializers.CharField(source='hire_confirmation.application.job.title', read_only=True)
    job_location = serializers.CharField(source='hire_confirmation.application.job.location', read_only=True)
    salary_min = serializers.IntegerField(source='hire_confirmation.application.job.salary_min', read_only=True)
    salary_max = serializers.IntegerField(source='hire_confirmation.application.job.salary_max', read_only=True)
    employer_name = serializers.CharField(source='employer.name', read_only=True)
    hire_finalized_at = serializers.DateTimeField(source='hire_confirmation.hire_finalized_at', read_only=True)

    class Meta:
        model = Commission
        fields = ['id', 'candidate_first_name', 'candidate_last_name', 'candidate_email', 'job_title',
                  'job_location', 'salary_min', 'salary_max', 'employer_name', 'amount', 'rate', 'status',
                  'hire_finalized_at', 'created_at', 'invoiced_at', 'paid_at', 'refunded_at']
        read_only_fields = ['id', 'candidate_first_name', 'candidate_last_name', 'candidate_email', 'job_title',
                           'job_location', 'salary_min', 'salary_max', 'employer_name', 'amount', 'rate',
                           'hire_finalized_at', 'created_at', 'invoiced_at', 'paid_at', 'refunded_at']
