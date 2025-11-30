from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # FontAwesome class

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class Counselor(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    additional_info = models.TextField()
    email = models.EmailField()
    image = models.ImageField(upload_to='counselors/')

    def __str__(self):
        return self.name

class SupportResource(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic Support'),
        ('mental_health', 'Mental Health & Wellbeing'),
        ('career', 'Career Guidance'),
        ('other', 'Other Resources')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='academic')
    file = models.FileField(upload_to='support_resources/', blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    icon = models.CharField(max_length=50, default='file-alt', help_text="FontAwesome icon name (e.g., file-pdf)")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class AppointmentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    counselor = models.ForeignKey(Counselor, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_date = models.DateField(help_text="Preferred date for the appointment")
    preferred_time = models.TimeField(help_text="Preferred time", null=True, blank=True)
    reason = models.TextField(help_text="Briefly describe why you'd like to meet")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True, help_text="Internal notes for counselors")
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Appointment: {self.student_name} - {self.status}"