from rest_framework import serializers
from jobs.application_models import JobApplication


class ApplicationReviewListSerializer(serializers.ModelSerializer):
    candidate_first_name = serializers.CharField(source='candidate.first_name', read_only=True)
    candidate_last_name = serializers.CharField(source='candidate.last_name', read_only=True)
    candidate_id = serializers.IntegerField(source='candidate.id', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_id = serializers.IntegerField(source='job.id', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'candidate_id', 'candidate_first_name', 'candidate_last_name', 'job_id', 'job_title',
                  'status', 'created_at', 'updated_at', 'reviewed_at']
        read_only_fields = ['id', 'candidate_id', 'candidate_first_name', 'candidate_last_name', 'job_id',
                           'job_title', 'created_at', 'updated_at', 'reviewed_at']


class ApplicationReviewDetailSerializer(serializers.ModelSerializer):
    candidate_first_name = serializers.CharField(source='candidate.first_name', read_only=True)
    candidate_last_name = serializers.CharField(source='candidate.last_name', read_only=True)
    candidate_id = serializers.IntegerField(source='candidate.id', read_only=True)
    candidate_location = serializers.CharField(source='candidate.location', read_only=True)
    candidate_phone = serializers.CharField(source='candidate.phone', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_id = serializers.IntegerField(source='job.id', read_only=True)
    job_description = serializers.CharField(source='job.description', read_only=True)
    job_location = serializers.CharField(source='job.location', read_only=True)
    job_salary_min = serializers.IntegerField(source='job.salary_min', read_only=True)
    job_salary_max = serializers.IntegerField(source='job.salary_max', read_only=True)
    rejection_reason = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'candidate_id', 'candidate_first_name', 'candidate_last_name', 'candidate_location',
                  'candidate_phone', 'job_id', 'job_title', 'job_description', 'job_location', 'job_salary_min',
                  'job_salary_max', 'status', 'cover_letter', 'rejection_reason', 'created_at', 'updated_at',
                  'reviewed_at', 'hired_at']
        read_only_fields = ['id', 'candidate_id', 'candidate_first_name', 'candidate_last_name', 'candidate_location',
                           'candidate_phone', 'job_id', 'job_title', 'job_description', 'job_location',
                           'job_salary_min', 'job_salary_max', 'cover_letter', 'created_at', 'updated_at',
                           'reviewed_at', 'hired_at']


class ReviewApplicationSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['reviewed', 'rejected'])
    rejection_reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate(self, data):
        if data.get('status') == 'rejected' and not data.get('rejection_reason'):
            raise serializers.ValidationError("Rejection reason is required when rejecting an application.")
        return data
