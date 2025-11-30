from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatConversation(models.Model):
    """Stores chat conversation sessions"""
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    message_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Chat Conversation'
        verbose_name_plural = 'Chat Conversations'
    
    def __str__(self):
        return f"Conversation {self.session_id[:8]}... ({self.started_at.strftime('%Y-%m-%d %H:%M')})"


class ChatMessage(models.Model):
    """Individual messages within conversations"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    conversation = models.ForeignKey(
        ChatConversation, 
        related_name='messages', 
        on_delete=models.CASCADE
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Optional: store context used for this response
    context_used = models.TextField(blank=True, help_text="Context retrieved from database")
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class ChatFAQ(models.Model):
    """Admin-managed frequently asked questions with custom answers"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    keywords = models.CharField(
        max_length=500, 
        blank=True,
        help_text="Comma-separated keywords to match this FAQ"
    )
    priority = models.IntegerField(
        default=0, 
        help_text="Higher priority FAQs are checked first"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )
    
    class Meta:
        ordering = ['-priority', 'question']
        verbose_name = 'Chat FAQ'
        verbose_name_plural = 'Chat FAQs'
    
    def __str__(self):
        return self.question


class ChatAnalytics(models.Model):
    """Tracks popular questions and analytics"""
    question_hash = models.CharField(max_length=64, unique=True, db_index=True)
    question_sample = models.TextField()
    count = models.IntegerField(default=1)
    first_asked = models.DateTimeField(auto_now_add=True)
    last_asked = models.DateTimeField(auto_now=True)
    
    # Optional: track if question was answered successfully
    successful_responses = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-count']
        verbose_name = 'Chat Analytics'
        verbose_name_plural = 'Chat Analytics'
    
    def __str__(self):
        return f"{self.question_sample[:50]}... (asked {self.count} times)"
