# home/admin.py
from django.contrib import admin
from .models import CarouselImage, AboutUs, NewsArticle, NewsTicker, FacultyMember, PrincipalMessage, AboutUsSection, SiteConfiguration, PopupAnnouncement
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.html import format_html

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'caption', 'order', 'is_active']
    list_display_links = ['image_preview', 'caption']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['caption', 'alt_text', 'description']
    fields = ['order', 'image', 'caption', 'alt_text', 'description', 'action_url', 'is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 100px; object-fit: cover;" />'
        return "No image"
    image_preview.short_description = 'Preview'
    image_preview.allow_tags = True




class AboutUsSectionInline(admin.TabularInline):
    model = AboutUsSection
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20})},
    }

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    inlines = [AboutUsSectionInline]
    list_display = ['title']
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20})},
    }


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    search_fields = ('title',)


@admin.register(NewsTicker)
class NewsScrollAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)



class FacultyMemberAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('name', 'designation', 'category')
    
    # Add search functionality
    search_fields = ('name', 'designation')
    
    # Add filters for categories
    list_filter = ('category',)
    
    # Customize fields to be displayed in the detail view
    fields = ('name', 'designation', 'image', 'category')

# Register the FacultyMember model with the custom admin class
admin.site.register(FacultyMember, FacultyMemberAdmin)



class PrincipalMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'is_active')  # Display title, type, and active status
    list_filter = ('type', 'is_active')  # Filter by type and active status
    search_fields = ('title', 'message')  # Add search functionality for title and message
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
    fieldsets = (
        (None, {
            'fields': ('type', 'title', 'message', 'image', 'is_active')
        }),
    )

admin.site.register(PrincipalMessage, PrincipalMessageAdmin)

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'phone')
    fieldsets = (
        ('General', {
            'fields': ('site_name', 'logo', 'logo_footer', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('address', 'email', 'phone')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(PopupAnnouncement)
class PopupAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title', 'is_active', 'show_once_per_session', 'created_at']
    list_display_links = ['image_preview', 'title']
    list_filter = ['is_active', 'show_once_per_session']
    search_fields = ['title']
    readonly_fields = ['design_tips']
    
    fieldsets = (
        ('Design Guidance', {
            'fields': ('design_tips',),
            'description': 'Follow these tips to ensure your popups look premium and load fast.'
        }),
        ('Popup Content', {
            'fields': ('title', 'image', 'link')
        }),
        ('Settings', {
            'fields': ('is_active', 'show_once_per_session')
        }),
    )

    def design_tips(self, obj):
        return format_html(
            '<div style="background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; color: #475569;">'
            '<h4 style="color: #0ea5e9; margin-top: 0;">🚀 Pro-Tips for Premium Banners:</h4>'
            '<ul style="margin-bottom: 0;">'
                '<li><b>Best Formats:</b> Use <b>PNG</b> for sharp text or <b>JPG</b> for colorful photos.</li>'
                '<li><b>File Size:</b> Keep images under <b>500KB</b> for instant loading.</li>'
                '<li><b>High-DPI:</b> Upload 1600px wide images for perfect clarity on iPhone/Retina screens.</li>'
            '</ul>'
            '</div>'
        )
    design_tips.short_description = 'Professional Guidance'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'
