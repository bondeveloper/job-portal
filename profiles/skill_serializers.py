from rest_framework import serializers
from .skill_models import Skill, CandidateSkill
from .models import CandidateProfile


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class CandidateSkillSerializer(serializers.Serializer):
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True
    )
    skills = SkillSerializer(many=True, read_only=True, source='skill_set')

    def validate_skill_ids(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("At least 1 skill is required")
        if len(value) > 10:
            raise serializers.ValidationError("Maximum 10 skills allowed")
        return value

    def save(self, profile):
        skill_ids = self.validated_data.get('skill_ids', [])
        CandidateSkill.objects.filter(profile=profile).delete()
        for skill in skill_ids:
            CandidateSkill.objects.create(profile=profile, skill=skill)
        return profile
