from django.db import models
from jobs.application_models import JobApplication


class ApplicationReview(models.Model):
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='review')
    rejection_reason = models.TextField(blank=True, max_length=500)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.application.candidate.user.email}'s application"
