from django.db import models
from .models import Employer
from jobs.hire_confirmation_models import HireConfirmation


class Commission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('invoiced', 'Invoiced'),
        ('disputed', 'Disputed'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    hire_confirmation = models.OneToOneField(HireConfirmation, on_delete=models.CASCADE, related_name='commission')
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='commissions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Commission amount in ZAR')
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00, help_text='Commission rate %')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invoiced_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employer', 'status']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Commission {self.id}: {self.amount} ZAR ({self.status})"
