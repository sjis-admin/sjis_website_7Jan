from django.contrib import admin
from .models import YearbookEdition

@admin.register(YearbookEdition)
class YearbookEditionAdmin(admin.ModelAdmin):
    """
    Simplified Yearbook Admin - Only handles PDF uploads for academic years.
    """
    list_display = ('year', 'title', 'is_published', 'pdf_file_status', 'created_at')
    list_filter = ('is_published', 'year')
    search_fields = ('title', 'year')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Yearbook Content', {
            'fields': ('year', 'title', 'pdf_file', 'cover_image')
        }),
        ('Publication Status', {
            'fields': ('is_published', 'published_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def pdf_file_status(self, obj):
        if obj.pdf_file:
            return "✅ Uploaded"
        return "❌ Missing"
    pdf_file_status.short_description = 'PDF Status'
