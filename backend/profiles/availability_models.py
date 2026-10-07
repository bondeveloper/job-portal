from django.db import models
from .models import CandidateProfile


class Availability(models.Model):
    EMPLOYMENT_TYPES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
    ]

    profile = models.OneToOneField(CandidateProfile, on_delete=models.CASCADE, related_name='availability_details')
    available_from_month = models.IntegerField()  # 1-12
    available_from_year = models.IntegerField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    salary_min = models.IntegerField(blank=True, null=True)  # ZAR
    salary_max = models.IntegerField(blank=True, null=True)  # ZAR
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'availability'

    def __str__(self):
        return f"{self.profile.user.email} - {self.employment_type}"
