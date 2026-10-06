from django.db import models
from .models import Employer
from jobs.application_models import JobApplication


class ApplicationShortlist(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='application_shortlists')
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employer', 'application')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employer', '-created_at']),
        ]

    def __str__(self):
        return f"{self.employer.name} shortlisted {self.application.candidate.user.email}"
