from .models import CandidateProfile
from .skill_models import CandidateSkill
from .availability_models import Availability


def is_profile_complete(profile):
    """
    Check if a profile has all required fields for searchability.
    Required: first_name, last_name, location, ≥1 skill, availability (month/year + type)
    Optional: phone, work_history, salary
    """
    # Check basic fields
    if not profile.first_name or not profile.last_name or not profile.location:
        return False

    # Check at least 1 skill
    if not CandidateSkill.objects.filter(profile=profile).exists():
        return False

    # Check availability
    try:
        availability = Availability.objects.get(profile=profile)
        if not availability.available_from_month or not availability.available_from_year or not availability.employment_type:
            return False
    except Availability.DoesNotExist:
        return False

    return True


def update_profile_status(profile):
    """
    Update profile status based on completeness.
    - If profile is complete and status is 'pending', transition to 'active'
    - If profile becomes incomplete, transition 'active' → 'pending'
    """
    is_complete = is_profile_complete(profile)

    if is_complete and profile.status == 'pending':
        profile.status = 'active'
        profile.save(update_fields=['status', 'updated_at'])
        return True
    elif not is_complete and profile.status == 'active':
        profile.status = 'pending'
        profile.save(update_fields=['status', 'updated_at'])
        return True

    return False
