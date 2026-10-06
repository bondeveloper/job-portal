from rest_framework import serializers
from .application_shortlist_models import ApplicationShortlist


class ApplicationShortlistSerializer(serializers.ModelSerializer):
    candidate_first_name = serializers.CharField(source='application.candidate.first_name', read_only=True)
    candidate_last_name = serializers.CharField(source='application.candidate.last_name', read_only=True)
    candidate_id = serializers.IntegerField(source='application.candidate.id', read_only=True)
    application_id = serializers.IntegerField(source='application.id', read_only=True)
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    job_id = serializers.IntegerField(source='application.job.id', read_only=True)
    application_status = serializers.CharField(source='application.status', read_only=True)

    class Meta:
        model = ApplicationShortlist
        fields = ['id', 'candidate_id', 'candidate_first_name', 'candidate_last_name', 'application_id',
                  'job_id', 'job_title', 'application_status', 'created_at']
        read_only_fields = ['id', 'candidate_id', 'candidate_first_name', 'candidate_last_name', 'application_id',
                           'job_id', 'job_title', 'application_status', 'created_at']


class AddToApplicationShortlistSerializer(serializers.Serializer):
    application_id = serializers.IntegerField()

    def validate_application_id(self, value):
        if not JobApplication.objects.filter(id=value).exists():
            raise serializers.ValidationError("Application not found.")
        return value
