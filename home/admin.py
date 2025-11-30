# home/admin.py
from django.contrib import admin
from .models import CarouselImage, AboutUs, NewsArticle, NewsTicker, FacultyMember, PrincipalMessage, AboutUsSection, SiteConfiguration
from tinymce.widgets import TinyMCE
from django.db import models

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
            'fields': ('site_name', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('address', 'email', 'phone')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
