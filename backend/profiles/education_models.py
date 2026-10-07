from django.db import models
from .models import CandidateProfile


class Education(models.Model):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, help_text='e.g., Bachelor of Science')
    field = models.CharField(max_length=255, help_text='e.g., Computer Science')
    graduation_date = models.DateField()
    description = models.TextField(blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'education'
        ordering = ['-graduation_date']

    def __str__(self):
        return f"{self.profile.user.email} - {self.degree} at {self.institution}"
