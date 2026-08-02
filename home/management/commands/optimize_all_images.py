from django.core.management.base import BaseCommand
from home.models import FacultyMember, CarouselImage

class Command(BaseCommand):
    help = 'Bulk optimizes and converts all Carousel/Slider and Faculty images to WebP'

    def handle(self, *args, **options):
        # 1. Carousel Slider Images
        carousels = CarouselImage.objects.filter(media_type='image')
        c_total = carousels.count()
        self.stdout.write(f"Starting bulk WebP optimization for {c_total} hero slider images...")
        c_count = 0
        for slide in carousels:
            if slide.image:
                try:
                    slide.save()
                    c_count += 1
                    self.stdout.write(f"[{c_count}/{c_total}] Optimized slider image: {slide.caption or slide.id}")
                except Exception as e:
                    self.stderr.write(f"Failed slider image {slide.id}: {e}")

        # 2. Faculty Images
        members = FacultyMember.objects.all()
        f_total = members.count()
        self.stdout.write(f"Starting bulk WebP optimization for {f_total} faculty images...")
        f_count = 0
        for member in members:
            if member.image:
                try:
                    member.save()
                    f_count += 1
                    self.stdout.write(f"[{f_count}/{f_total}] Optimized faculty image: {member.name}")
                except Exception as e:
                    self.stderr.write(f"Failed faculty image {member.name}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Successfully converted {c_count} slider images and {f_count} faculty images to WebP!"))
