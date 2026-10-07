from rest_framework import serializers
from .application_models import JobApplication
from profiles.serializers import CandidateProfileSerializer


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_id = serializers.IntegerField(source='job.id', read_only=True)
    company_name = serializers.CharField(source='job.employer.name', read_only=True)
    location = serializers.CharField(source='job.location', read_only=True)
    salary_min = serializers.IntegerField(source='job.salary_min', read_only=True)
    salary_max = serializers.IntegerField(source='job.salary_max', read_only=True)
    candidate_email = serializers.CharField(source='candidate.user.email', read_only=True)
    candidate_name = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = [
            'id', 'job_id', 'job_title', 'company_name', 'location', 'salary_min', 'salary_max',
            'candidate_email', 'candidate_name', 'status', 'cover_letter',
            'created_at', 'updated_at', 'shortlisted_at', 'rejected_at', 'withdrawn_at'
        ]
        read_only_fields = [
            'id', 'job_id', 'job_title', 'company_name', 'location', 'salary_min', 'salary_max',
            'candidate_email', 'candidate_name', 'status', 'created_at', 'updated_at',
            'shortlisted_at', 'rejected_at', 'withdrawn_at'
        ]

    def get_candidate_name(self, obj):
        return f"{obj.candidate.first_name} {obj.candidate.last_name}"


class SubmitApplicationSerializer(serializers.Serializer):
    cover_letter = serializers.CharField(max_length=2000, required=False, allow_blank=True)

    def validate_cover_letter(self, value):
        if value and len(value.strip()) == 0:
            raise serializers.ValidationError("Cover letter cannot be empty.")
        return value


class ApplicationStatusUpdateSerializer(serializers.Serializer):
    STATUS_CHOICES = [
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)
