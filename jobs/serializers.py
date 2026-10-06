from rest_framework import serializers
from employers.job_models import Job, JobSkill


class JobSkillDisplaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='skill.name', read_only=True)
    skill_id = serializers.IntegerField(source='skill.id', read_only=True)

    class Meta:
        model = JobSkill
        fields = ['skill_id', 'name']


class JobSearchSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='employer.name', read_only=True)
    required_skills = JobSkillDisplaySerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary_min', 'salary_max',
                  'experience_level', 'company_name', 'required_skills', 'created_at']
        read_only_fields = ['id', 'created_at']
