from rest_framework import serializers
from .job_models import Job, JobSkill
from profiles.skill_models import Skill


class JobSkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='skill.name', read_only=True)
    skill_id = serializers.IntegerField(source='skill.id', read_only=True)

    class Meta:
        model = JobSkill
        fields = ['skill_id', 'name']


class JobSerializer(serializers.ModelSerializer):
    required_skills = JobSkillSerializer(many=True, read_only=True)
    required_skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary_min', 'salary_max',
                  'experience_level', 'status', 'required_skills', 'required_skill_ids',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('salary_min') and data.get('salary_max'):
            if data['salary_min'] > data['salary_max']:
                raise serializers.ValidationError("Salary min cannot be greater than salary max.")
        return data

    def create(self, validated_data):
        skill_ids = validated_data.pop('required_skill_ids', [])
        job = Job.objects.create(**validated_data)
        for skill in skill_ids:
            JobSkill.objects.create(job=job, skill=skill)
        return job

    def update(self, instance, validated_data):
        skill_ids = validated_data.pop('required_skill_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if skill_ids is not None:
            instance.required_skills.all().delete()
            for skill in skill_ids:
                JobSkill.objects.create(job=instance, skill=skill)

        return instance
