# home/models.py
from django.db import models
from tinymce.models import HTMLField

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, help_text="Optional description shown on the slide")
    action_url = models.URLField(blank=True, help_text="Optional URL for 'Learn More' button")
    order = models.PositiveIntegerField(default=0, help_text="Order of appearance (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this slide")
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Slider Image'
        verbose_name_plural = 'Slider Images'

    def __str__(self):
        return self.caption or self.alt_text or f"Slide {self.id}"



class AboutUs(models.Model):
    title = models.CharField(max_length=255, default="About Us")
    short_description = HTMLField(help_text="This will be shown on the home page.")
    long_description = HTMLField(help_text="This will be shown on the detailed page.")
    main_image = models.ImageField(
        upload_to='about_us/', 
        default='path/to/default/main_image.jpg', 
        help_text="Main image for the home page."
    )
    additional_images = models.ImageField(
        upload_to='about_us/', 
        blank=True, 
        null=True, 
        help_text="Additional images for the detailed page."
    )

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def __str__(self):
        return self.title


class AboutUsSection(models.Model):
    about_us = models.ForeignKey(AboutUs, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # E.g., "Mission", "Vision", "Goal"
    content = HTMLField()

    def __str__(self):
        return f"{self.about_us.title} - {self.title}"



class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    published_date = models.DateField()
    
    def __str__(self):
        return self.title


class NewsTicker(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    content = models.FileField(upload_to='news/', blank=True, null=True)  # Allows PDF/image upload

    def __str__(self):
        return self.title


class FacultyMember(models.Model):
    CATEGORY_CHOICES = [
        ('Administration', 'Administration'),
        ('Teacher', 'Teacher'),
        ('Office Staff', 'Office Staff'),
    ]

    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='faculty_images/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class PrincipalMessage(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('Principal', "Principal's Message"),
        ('VicePrincipal', "Vice-Principal's Message"),
    ]

    title = models.CharField(max_length=200, help_text="Title of the message")
    message = models.TextField(help_text="The main message")
    image = models.ImageField(upload_to='principal_images/', blank=True, null=True, help_text="Optional: Upload an image")
    is_active = models.BooleanField(default=True, help_text="Mark as active to display")
    type = models.CharField(
        max_length=20, 
        choices=MESSAGE_TYPE_CHOICES, 
        default='Principal', 
        help_text="Select the type of message"
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=255, default="St. Joseph International School")
    logo = models.ImageField(upload_to='site_config/', help_text="Upload the school logo here")
    favicon = models.ImageField(upload_to='site_config/', blank=True, null=True, help_text="Upload the favicon here")
    
    # Contact Info
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteConfiguration.objects.exists():
            # If you want to ensure only one instance exists, you can raise an error
            # or just update the existing one. For simplicity in admin, we might just let it be
            # but usually singleton is better.
            return super(SiteConfiguration, self).save(*args, **kwargs)
        return super(SiteConfiguration, self).save(*args, **kwargs)










