from django.db import models
from django.utils import timezone
from .application_models import JobApplication


class HireConfirmation(models.Model):
    STATUS_CHOICES = [
        ('employer_confirmed', 'Employer Confirmed, Awaiting Candidate'),
        ('confirmed', 'Mutually Confirmed'),
        ('declined', 'Declined'),
    ]

    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='hire_confirmation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='employer_confirmed')

    # Confirmations
    employer_confirmed_at = models.DateTimeField(auto_now_add=True)
    candidate_confirmed_at = models.DateTimeField(null=True, blank=True)

    # Timeline
    hire_finalized_at = models.DateTimeField(null=True, blank=True, help_text='Hire finalized after 30 days; no new refunds allowed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hire_confirmations'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Hire confirmation for {self.application.candidate.user.email} - {self.status}"

    def candidate_confirm(self):
        """Candidate confirms the hire. Triggers commission creation."""
        self.candidate_confirmed_at = timezone.now()
        self.status = 'confirmed'
        self.save()
        # Commission creation will be handled by signals
        return self

    def is_mutual(self):
        """Check if both parties have confirmed."""
        return self.status == 'confirmed' and self.candidate_confirmed_at is not None

    def can_request_refund(self):
        """Check if refund can be requested (within 30 days of confirmation)."""
        if not self.is_mutual():
            return False
        days_since_confirmation = (timezone.now() - self.candidate_confirmed_at).days
        return days_since_confirmation <= 30

    def finalize_hire(self):
        """Finalize hire after 30 days - closes dispute window."""
        self.hire_finalized_at = timezone.now()
        self.save()
