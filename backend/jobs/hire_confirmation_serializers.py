from rest_framework import serializers
from .hire_confirmation_models import HireConfirmation


class HireConfirmationSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='application.job.employer.name', read_only=True)
    candidate_email = serializers.CharField(source='application.candidate.user.email', read_only=True)
    candidate_name = serializers.SerializerMethodField()
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    job_location = serializers.CharField(source='application.job.location', read_only=True)
    job_salary_min = serializers.IntegerField(source='application.job.salary_min', read_only=True)
    job_salary_max = serializers.IntegerField(source='application.job.salary_max', read_only=True)
    is_mutual = serializers.SerializerMethodField()
    can_request_refund = serializers.SerializerMethodField()

    class Meta:
        model = HireConfirmation
        fields = [
            'id', 'status', 'employer_name', 'candidate_email', 'candidate_name',
            'job_title', 'job_location', 'job_salary_min', 'job_salary_max',
            'employer_confirmed_at', 'candidate_confirmed_at', 'hire_finalized_at',
            'is_mutual', 'can_request_refund', 'created_at'
        ]
        read_only_fields = [
            'id', 'status', 'employer_name', 'candidate_email', 'candidate_name',
            'job_title', 'job_location', 'job_salary_min', 'job_salary_max',
            'employer_confirmed_at', 'candidate_confirmed_at', 'hire_finalized_at',
            'is_mutual', 'can_request_refund', 'created_at'
        ]

    def get_candidate_name(self, obj):
        profile = obj.application.candidate
        return f"{profile.first_name} {profile.last_name}"

    def get_is_mutual(self, obj):
        return obj.is_mutual()

    def get_can_request_refund(self, obj):
        return obj.can_request_refund()


class CandidateConfirmHireSerializer(serializers.Serializer):
    """Serializer for candidate confirming a hire."""
    pass
