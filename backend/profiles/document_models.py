from django.db import models
from django.core.validators import FileExtensionValidator
from .models import CandidateProfile


class SupportingDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('cover_letter', 'Cover Letter'),
        ('portfolio', 'Portfolio Sample'),
        ('certificate', 'Certificate/Credential'),
        ('reference', 'Reference Document'),
        ('other', 'Other'),
    ]

    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='supporting_documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(
        upload_to='supporting_documents/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    file_size = models.IntegerField(help_text='File size in bytes')
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supporting_documents'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'document_type', 'file_name'],
                name='unique_document_per_candidate'
            )
        ]

    def __str__(self):
        return f"{self.profile.user.email} - {self.get_document_type_display()}"

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.file_name = self.file.name
        super().save(*args, **kwargs)
