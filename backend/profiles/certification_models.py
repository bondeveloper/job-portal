from django.db import models
from .models import CandidateProfile


class Certification(models.Model):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, help_text='e.g., AWS, Google, CompTIA')
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True, help_text='Leave blank if no expiry')
    credential_id = models.CharField(max_length=255, blank=True, null=True, help_text='Certification reference number')
    credential_url = models.URLField(blank=True, null=True, help_text='Link to verify credential')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'certifications'
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.profile.user.email} - {self.name}"

    @property
    def is_expired(self):
        if not self.expiry_date:
            return False
        from django.utils import timezone
        return self.expiry_date < timezone.now().date()
