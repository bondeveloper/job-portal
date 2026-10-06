from rest_framework import serializers
from .shortlist_models import CandidateShortlist
from profiles.models import CandidateProfile


class ShortlistCandidateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='candidate.first_name', read_only=True)
    last_name = serializers.CharField(source='candidate.last_name', read_only=True)
    location = serializers.CharField(source='candidate.location', read_only=True)
    phone = serializers.CharField(source='candidate.phone', read_only=True)
    candidate_id = serializers.IntegerField(source='candidate.id', read_only=True)

    class Meta:
        model = CandidateShortlist
        fields = ['id', 'candidate_id', 'first_name', 'last_name', 'location', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']


class AddToShortlistSerializer(serializers.Serializer):
    candidate_id = serializers.IntegerField()

    def validate_candidate_id(self, value):
        if not CandidateProfile.objects.filter(id=value).exists():
            raise serializers.ValidationError("Candidate not found.")
        return value
