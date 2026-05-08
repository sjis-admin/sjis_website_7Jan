from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class YearbookEdition(models.Model):
    """Represents a yearbook for a specific academic year with a PDF upload"""
    year = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        help_text="Academic year (e.g., 2024 for 2024-2025)"
    )
    title = models.CharField(max_length=200, help_text="e.g., 'Memories 2024-2025'")
    cover_image = models.ImageField(upload_to='yearbook/covers/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='yearbook/pdfs/', blank=True, null=True, help_text="Full yearbook PDF")
    published_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=False, help_text="Make this yearbook visible to the public")
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
