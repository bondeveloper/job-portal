from django.db import models
from .application_models import JobApplication


class HireConfirmation(models.Model):
    STATUS_CHOICES = [
        ('pending_candidate', 'Pending Candidate'),
        ('pending_employer', 'Pending Employer'),
        ('confirmed', 'Confirmed'),
        ('declined', 'Declined'),
    ]

    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='hire_confirmation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_candidate')
    employer_confirmed = models.BooleanField(default=True)
    candidate_confirmed = models.BooleanField(default=False)
    employer_confirmed_at = models.DateTimeField(auto_now_add=True)
    candidate_confirmed_at = models.DateTimeField(null=True, blank=True)
    hire_finalized_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hire confirmation for {self.application.candidate.user.email} - {self.status}"
