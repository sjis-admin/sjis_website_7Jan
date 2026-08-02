from django.core.management.base import BaseCommand
from home.models import FacultyMember

class Command(BaseCommand):
    help = 'Bulk optimizes and compresses all existing Faculty Member profile images'

    def handle(self, *args, **options):
        members = FacultyMember.objects.all()
        total = members.count()
        self.stdout.write(f"Starting bulk optimization for {total} faculty images...")
        
        count = 0
        for member in members:
            if member.image:
                try:
                    member.save()
                    count += 1
                    self.stdout.write(f"[{count}/{total}] Optimized image for: {member.name}")
                except Exception as e:
                    self.stderr.write(f"Failed to optimize image for {member.name}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Successfully optimized {count} faculty images!"))
