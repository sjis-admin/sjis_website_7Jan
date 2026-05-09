from django.contrib import admin
from django.utils.html import format_html
from .models import YearbookEdition

@admin.register(YearbookEdition)
class YearbookEditionAdmin(admin.ModelAdmin):
    """
    Simplified Yearbook Admin - Only handles PDF uploads for academic years.
    """
    list_display = ('year', 'title', 'is_published', 'pdf_file_status', 'created_at')
    list_filter = ('is_published', 'year')
    search_fields = ('title', 'year')
    readonly_fields = ('upload_guidance', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Optimization Guide', {
            'fields': ('upload_guidance',),
            'description': 'Important tips for handling large magazine PDFs.'
        }),
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

    def upload_guidance(self, obj):
        return format_html(
            '<div style="background: #fdf2f2; padding: 15px; border-radius: 8px; border: 1px solid #fee2e2; color: #991b1b;">'
            '<h4 style="margin-top: 0; color: #b91c1c;">📚 Handling Large Magazines:</h4>'
            '<ul style="margin-bottom: 0;">'
                '<li><b>Server Limit:</b> I have configured the system to handle up to <b>500MB</b> per file.</li>'
                '<li><b>User Experience:</b> If a PDF is too large (e.g., 200MB+), it will load very slowly for students on mobile.</li>'
                '<li><b>Optimization:</b> Always use a tool like <a href="https://www.ilovepdf.com/compress_pdf" target="_blank" style="color: #b91c1c; text-decoration: underline;">IlovePDF (Compress PDF)</a> before uploading. Aim for under <b>50MB</b> for best results.</li>'
            '</ul>'
            '</div>'
        )
    upload_guidance.short_description = 'Professional Guidance'
