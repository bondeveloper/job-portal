from django.db import models
from .models import CandidateProfile


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skills'
        ordering = ['name']

    def __str__(self):
        return self.name


class CandidateSkill(models.Model):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'candidate_skills'
        unique_together = ('profile', 'skill')

    def __str__(self):
        return f"{self.profile.user.email} - {self.skill.name}"
