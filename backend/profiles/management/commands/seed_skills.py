from django.core.management.base import BaseCommand
from profiles.skill_models import Skill
from profiles.skills_data import PREDEFINED_SKILLS


class Command(BaseCommand):
    help = 'Seed the database with predefined skills'

    def handle(self, *args, **options):
        created_count = 0
        for skill_name in PREDEFINED_SKILLS:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} skills'))
