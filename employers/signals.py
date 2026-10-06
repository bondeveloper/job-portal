from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from jobs.hire_confirmation_models import HireConfirmation
from .commission_models import Commission


@receiver(post_save, sender=HireConfirmation)
def create_commission_on_hire(sender, instance, created, **kwargs):
    """Auto-create Commission when HireConfirmation is confirmed."""
    if not created and instance.status == 'confirmed':
        employer = instance.application.job.employer
        salary_min = instance.application.job.salary_min
        commission_rate = 10.00
        commission_amount = (salary_min * commission_rate) / 100

        Commission.objects.update_or_create(
            hire_confirmation=instance,
            defaults={
                'employer': employer,
                'amount': commission_amount,
                'rate': commission_rate,
                'status': 'pending',
            }
        )
