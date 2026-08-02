from django.core.management.base import BaseCommand
from home.models import FacultyMember, CarouselImage, NewsArticle, PrincipalMessage, PopupAnnouncement

class Command(BaseCommand):
    help = 'Bulk optimizes and converts all website images (News, Hero Sliders, Faculty, Messages, Popups) to WebP format'

    def handle(self, *args, **options):
        # 1. News Article Images
        news = NewsArticle.objects.all()
        n_total = news.count()
        self.stdout.write(f"Starting bulk WebP optimization for {n_total} news article images...")
        n_count = 0
        for article in news:
            if article.image:
                try:
                    article.save()
                    n_count += 1
                    self.stdout.write(f"[{n_count}/{n_total}] Optimized News image: {article.title[:30]}")
                except Exception as e:
                    self.stderr.write(f"Failed News image {article.title}: {e}")

        # 2. Carousel Slider Images
        carousels = CarouselImage.objects.filter(media_type='image')
        c_total = carousels.count()
        self.stdout.write(f"Starting bulk WebP optimization for {c_total} hero slider images...")
        c_count = 0
        for slide in carousels:
            if slide.image:
                try:
                    slide.save()
                    c_count += 1
                    self.stdout.write(f"[{c_count}/{c_total}] Optimized Slider image: {slide.caption or slide.id}")
                except Exception as e:
                    self.stderr.write(f"Failed Slider image {slide.id}: {e}")

        # 3. Faculty Images
        members = FacultyMember.objects.all()
        f_total = members.count()
        self.stdout.write(f"Starting bulk WebP optimization for {f_total} faculty images...")
        f_count = 0
        for member in members:
            if member.image:
                try:
                    member.save()
                    f_count += 1
                    self.stdout.write(f"[{f_count}/{f_total}] Optimized Faculty image: {member.name}")
                except Exception as e:
                    self.stderr.write(f"Failed Faculty image {member.name}: {e}")

        # 4. Principal Messages
        msgs = PrincipalMessage.objects.all()
        for msg in msgs:
            if msg.image:
                msg.save()

        # 5. Popups
        popups = PopupAnnouncement.objects.all()
        for popup in popups:
            if popup.image or popup.desktop_image:
                popup.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully converted {n_count} news images, {c_count} slider images, and {f_count} faculty images to WebP!"))
