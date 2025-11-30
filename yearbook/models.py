from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class YearbookEdition(models.Model):
    """Represents a yearbook for a specific academic year"""
    year = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        help_text="Academic year (e.g., 2024 for 2024-2025)"
    )
    title = models.CharField(max_length=200, help_text="e.g., 'Memories 2024-2025'")
    cover_image = models.ImageField(upload_to='yearbook/covers/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=False, help_text="Make this yearbook visible to the public")
    pdf_file = models.FileField(upload_to='yearbook/pdfs/', blank=True, null=True, help_text="Full yearbook PDF")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year']
        verbose_name = 'Yearbook Edition'
        verbose_name_plural = 'Yearbook Editions'
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    @property
    def academic_year(self):
        """Returns formatted academic year string"""
        return f"{self.year}-{self.year + 1}"


class YearbookSection(models.Model):
    """Sections within a yearbook (e.g., 'Grade 10', 'Faculty', 'Events')"""
    yearbook = models.ForeignKey(YearbookEdition, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Material icon name")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Yearbook Section'
        verbose_name_plural = 'Yearbook Sections'
    
    def __str__(self):
        return f"{self.yearbook.year} - {self.title}"


class YearbookPhoto(models.Model):
    """Individual photos in the yearbook"""
    section = models.ForeignKey(YearbookSection, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='yearbook/photos/')
    caption = models.CharField(max_length=500, blank=True, null=True)
    student_name = models.CharField(max_length=200, blank=True, null=True)
    student_class = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 'Grade 10A'")
    order = models.IntegerField(default=0, help_text="Display order within section")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
        verbose_name = 'Yearbook Photo'
        verbose_name_plural = 'Yearbook Photos'
    
    def __str__(self):
        if self.student_name:
            return f"{self.student_name} - {self.section.title}"
        return f"Photo in {self.section.title}"


class YearbookMessage(models.Model):
    """Messages from principal, teachers, etc."""
    yearbook = models.ForeignKey(YearbookEdition, on_delete=models.CASCADE, related_name='messages')
    author = models.CharField(max_length=200, help_text="Name of the person")
    position = models.CharField(max_length=200, help_text="e.g., 'Principal', 'Vice Principal'")
    message = models.TextField()
    photo = models.ImageField(upload_to='yearbook/messages/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order', 'author']
        verbose_name = 'Yearbook Message'
        verbose_name_plural = 'Yearbook Messages'
    
    def __str__(self):
        return f"{self.author} - {self.yearbook.year}"


class YearbookQuote(models.Model):
    """Student quotes and memories"""
    yearbook = models.ForeignKey(YearbookEdition, on_delete=models.CASCADE, related_name='quotes')
    student_name = models.CharField(max_length=200)
    student_class = models.CharField(max_length=100)
    quote = models.TextField(max_length=500)
    photo = models.ImageField(upload_to='yearbook/quotes/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Show on main yearbook page")
    
    class Meta:
        verbose_name = 'Student Quote'
        verbose_name_plural = 'Student Quotes'
    
    def __str__(self):
        return f"{self.student_name} - {self.yearbook.year}"
