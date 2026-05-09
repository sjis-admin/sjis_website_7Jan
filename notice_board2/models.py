from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount
import bleach
from tinymce.models import HTMLField

# GRADE_CHOICES moved outside of the models for shared usage
GRADE_CHOICES = [
    ('3', 'Grade 3'),
    ('4', 'Grade 4'),
    ('5', 'Grade 5'),
    ('6', 'Grade 6'),
    ('7', 'Grade 7'),
    ('8', 'Grade 8'),
    ('9', 'Grade 9'),
    ('10', 'Grade 10'),
    ('AS', 'AS Level'),
    ('A', 'A Level'),
    ('Teachers', 'Teachers'),
    ('Staffs', 'Staffs')
]

class Grade(models.Model):
    name = models.CharField(max_length=100, choices=GRADE_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Grades"

class NoticeBoard(models.Model):
    title = models.CharField(max_length=202)
    content = HTMLField()
    
    # Target Grades - Using a ManyToManyField for multiple grade selection
    target_grades = models.ManyToManyField(
        'Grade',  # Reference the Grade model
        blank=True,
        related_name='notices_for_grade'
    )
    
    # Attachments (optional)
    attachment = models.FileField(
        upload_to='notice_attachments/',
        null=True,
        blank=True
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Hit Counter
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    ALLOWED_TAGS = [
        'p', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'br', 
        'span', 'blockquote', 'a', 'img', 'code', 'pre'
    ]
    ALLOWED_ATTRIBUTES = {
        'p': ['class'],
        'span': ['class'],
        'a': ['href', 'title', 'target'],  # Allow links
        'img': ['src', 'alt', 'title', 'width', 'height'],  # Allow images
        'code': ['class'],  # Allow code highlighting classes
    }

    def save(self, *args, **kwargs):
        """
        Sanitize HTML content before saving to ensure safe rendering.
        """
        if self.content:
            self.content = bleach.clean(
                self.content, 
                tags=self.ALLOWED_TAGS, 
                attributes=self.ALLOWED_ATTRIBUTES
            )
        super().save(*args, **kwargs)

    def get_safe_content(self):
        """
        Return sanitized content marked as safe for templates.
        """
        return mark_safe(self.content)

    @property
    def is_new(self):
        """
        Check if the notice is considered new (created today).
        """
        return self.created_at.date() == timezone.now().date()
    
    @property
    def formatted_target_grades(self):
        """
        Format multiple grades into a readable string, handling numeric and non-numeric grades.
        """
        # Get all grade names as a list of values (numeric or string)
        grade_values = list(self.target_grades.values_list('name', flat=True))
        
        # Handle no grades selected
        if not grade_values:
            return "No Specific Grade"
        
        # Handle all grades selected
        all_grade_values = [choice[0] for choice in GRADE_CHOICES]
        if set(grade_values) == set(all_grade_values):
            return "All Grades"
        
        # Check for Teachers or Staffs
        if 'Teachers' in grade_values and 'Staffs' in grade_values:
            return "Teachers and Staffs"
        elif 'Teachers' in grade_values:
            return "Teachers"
        elif 'Staffs' in grade_values:
            return "Staffs"
        
        # Create a mapping for non-numeric grades
        grade_order = {grade[0]: i for i, grade in enumerate(GRADE_CHOICES, start=1)}
        
        # Sort grades based on the predefined order
        sorted_grades = sorted(grade_values, key=lambda x: grade_order.get(x, float('inf')))
        
        # Check for consecutive grades
        def is_consecutive(grades):
            order_values = [grade_order[g] for g in grades]
            return all(order_values[i+1] - order_values[i] == 1 for i in range(len(order_values)-1))
        
        # Format based on selection type
        if is_consecutive(sorted_grades):
            return f"{sorted_grades[0]} to {sorted_grades[-1]}"
        elif len(sorted_grades) <= 2:
            return ', '.join(sorted_grades)
        else:
            return ', '.join(sorted_grades)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Notice Board Entries"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('notice_board2:detail', args=[str(self.id)])
