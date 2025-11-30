"""
Admin interface for chatbot management.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import ChatConversation, ChatMessage, ChatFAQ, ChatAnalytics


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ('session_id_short', 'started_at', 'message_count', 'last_message_at', 'user_ip')
    list_filter = ('started_at', 'last_message_at')
    search_fields = ('session_id', 'user_ip')
    readonly_fields = ('session_id', 'user_ip', 'user_agent', 'started_at', 'last_message_at', 'message_count')
    date_hierarchy = 'started_at'
    
    def session_id_short(self, obj):
        return f"{obj.session_id[:8]}..."
    session_id_short.short_description = 'Session ID'
    
    def has_add_permission(self, request):
        return False


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'timestamp', 'context_used')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation_short', 'role', 'content_preview', 'timestamp')
    list_filter = ('role', 'timestamp')
    search_fields = ('content', 'conversation__session_id')
    readonly_fields = ('conversation', 'role', 'content', 'timestamp', 'context_used')
    date_hierarchy = 'timestamp'
    
    def conversation_short(self, obj):
        return f"{obj.conversation.session_id[:8]}..."
    conversation_short.short_description = 'Conversation'
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def has_add_permission(self, request):
        return False


@admin.register(ChatFAQ)
class ChatFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'priority', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'priority')
    search_fields = ('question', 'answer', 'keywords')
    list_editable = ('is_active', 'priority')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('FAQ Content', {
            'fields': ('question', 'answer', 'keywords')
        }),
        ('Settings', {
            'fields': ('priority', 'is_active', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ChatAnalytics)
class ChatAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'count', 'successful_responses', 'first_asked', 'last_asked')
    list_filter = ('first_asked', 'last_asked')
    search_fields = ('question_sample',)
    readonly_fields = ('question_hash', 'question_sample', 'count', 'first_asked', 'last_asked', 'successful_responses')
    date_hierarchy = 'last_asked'
    
    def question_preview(self, obj):
        return obj.question_sample[:60] + "..." if len(obj.question_sample) > 60 else obj.question_sample
    question_preview.short_description = 'Question'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion to clear analytics data
        return True
