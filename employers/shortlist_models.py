from django.db import models
from .models import Employer
from profiles.models import CandidateProfile


class CandidateShortlist(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='shortlisted_candidates')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employer', 'candidate')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employer.name} shortlisted {self.candidate.user.email}"
