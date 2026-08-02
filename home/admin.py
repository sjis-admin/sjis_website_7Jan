# home/admin.py
from django.contrib import admin
from .models import CarouselImage, AboutUs, NewsArticle, NewsTicker, FacultyMember, PrincipalMessage, AboutUsSection, SiteConfiguration, PopupAnnouncement
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.html import format_html
import csv
import zipfile
import io
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from django.http import HttpResponse
from PIL import Image
from django.http import HttpResponse

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'caption', 'media_type', 'order', 'is_active']
    list_display_links = ['image_preview', 'caption']
    list_editable = ['order', 'is_active']
    list_filter = ['media_type', 'is_active']
    search_fields = ['caption', 'alt_text', 'description']
    
    fieldsets = (
        ('Media Content', {
            'fields': ('media_type', 'image', 'video_file', 'youtube_url'),
            'description': 'Choose whether to display an image, a direct video file, or a YouTube video link.'
        }),
        ('Captions & Text', {
            'fields': ('caption', 'description', 'alt_text', 'action_url')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'





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



from PIL import ImageOps

class FacultyMemberAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('image_preview', 'name', 'designation', 'category', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    
    # Add search functionality
    search_fields = ('name', 'designation')
    
    # Add filters for categories
    list_filter = ('category',)
    
    # Customize fields to be displayed in the detail view
    fields = ('name', 'designation', 'image', 'category', 'order')
    
    actions = ['rotate_90_cw', 'rotate_90_ccw', 'rotate_180']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Photo'

    def _rotate_images(self, request, queryset, angle):
        count = 0
        for member in queryset:
            if member.image:
                try:
                    img = Image.open(member.image)
                    img = ImageOps.exif_transpose(img)
                    rotated_img = img.rotate(angle, expand=True)
                    
                    buffer = io.BytesIO()
                    if rotated_img.mode in ('RGBA', 'P'):
                        rotated_img = rotated_img.convert('RGB')
                    rotated_img.save(buffer, format='WEBP', quality=80, method=6)
                    buffer.seek(0)
                    
                    filename = member.image.name.split('/')[-1]
                    if not filename.lower().endswith('.webp'):
                        filename = filename.rsplit('.', 1)[0] + '.webp'
                        
                    member.image.save(filename, ContentFile(buffer.read()), save=True)
                    count += 1
                except Exception as e:
                    self.message_user(request, f"Failed to rotate image for {member.name}: {e}", level=messages.ERROR)
        if count > 0:
            self.message_user(request, f"Successfully rotated {count} faculty image(s) to WebP format.", level=messages.SUCCESS)

    @admin.action(description="🔄 Rotate selected photos 90° Clockwise (Right)")
    def rotate_90_cw(self, request, queryset):
        self._rotate_images(request, queryset, -90)

    @admin.action(description="🔄 Rotate selected photos 90° Counter-Clockwise (Left)")
    def rotate_90_ccw(self, request, queryset):
        self._rotate_images(request, queryset, 90)

    @admin.action(description="🔄 Rotate selected photos 180° (Flip Upside-Down)")
    def rotate_180(self, request, queryset):
        self._rotate_images(request, queryset, 180)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name='facultymember_bulk_upload'),
            path('bulk-upload/sample-csv/', self.admin_site.admin_view(self.download_sample_csv), name='facultymember_sample_csv'),
        ]
        return custom_urls + urls

    def download_sample_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="faculty_template.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['name', 'designation', 'category', 'image_filename'])
        writer.writerow(['John Doe', 'Mathematics Teacher', 'Teacher', 'john_doe.jpg'])
        writer.writerow(['Jane Smith', 'Principal', 'Administration', 'jane_smith.jpg'])
        writer.writerow(['Mike Johnson', 'Accountant', 'Office Staff', 'mike_johnson.jpg'])
        
        return response

    def bulk_upload_view(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            zip_file = request.FILES.get('zip_file')

            if not csv_file or not zip_file:
                messages.error(request, "Both CSV and ZIP files are required.")
                return redirect('..')

            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a valid CSV file.")
                return redirect('..')
                
            if not zip_file.name.endswith('.zip'):
                messages.error(request, "Please upload a valid ZIP file.")
                return redirect('..')

            try:
                # Read CSV
                csv_data = csv_file.read().decode('utf-8-sig') # Handle BOM if present
                csv_reader = csv.DictReader(io.StringIO(csv_data))
                
                # Read ZIP
                with zipfile.ZipFile(zip_file, 'r') as archive:
                    success_count = 0
                    errors = []
                    faculty_objects_to_create = []
                    
                    for row_num, row in enumerate(csv_reader, start=2): # start=2 because row 1 is header
                        # Clean column headers and values in case of spaces
                        row = {k.strip() if k else k: v.strip() if v else v for k, v in row.items()}
                        
                        name = row.get('name', '')
                        designation = row.get('designation', '')
                        category = row.get('category', '')
                        image_filename = row.get('image_filename', '')
                        
                        if not all([name, designation, category, image_filename]):
                            errors.append(f"Row {row_num}: Missing required fields. Ensure name, designation, category, and image_filename are present.")
                            continue
                            
                        # Try to find the image in zip
                        image_content = None
                        for name_in_zip in archive.namelist():
                            if name_in_zip.endswith(image_filename) and not name_in_zip.startswith('__MACOSX'):
                                image_content = archive.read(name_in_zip)
                                break
                                
                        if not image_content:
                            errors.append(f"Row {row_num} ({name}): Could not find image '{image_filename}' in the ZIP file.")
                            continue
                            
                        try:
                            # Open the image using Pillow to compress and resize
                            img = Image.open(io.BytesIO(image_content))
                            
                            # Convert to RGB if it's RGBA (PNG with transparency) to allow saving as JPEG/WebP safely if needed
                            if img.mode in ("RGBA", "P"):
                                img = img.convert("RGB")
                            
                            # Resize if the image is too large (max 800x800 for faculty photos)
                            img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                            
                            # Save back to a BytesIO object with extreme WebP compression
                            output_io = io.BytesIO()
                            img.save(output_io, format='WEBP', quality=80, method=6)
                            
                            # Change the extension to .webp for modern web optimization
                            safe_filename = image_filename.rsplit('.', 1)[0] + '.webp'
                            
                            faculty = FacultyMember(
                                name=name,
                                designation=designation,
                                category=category
                            )
                            # This writes the file to the media storage immediately, but does not hit the database
                            faculty.image.save(safe_filename, ContentFile(output_io.getvalue()), save=False)
                            
                            faculty_objects_to_create.append(faculty)
                            success_count += 1
                        except Exception as e:
                            errors.append(f"Row {row_num} ({name}): Failed to process image. Error: {str(e)}")
                            
                    # Solve N+1 inserts problem: Save all records in one single database query
                    if faculty_objects_to_create:
                        try:
                            FacultyMember.objects.bulk_create(faculty_objects_to_create)
                        except Exception as e:
                            errors.append(f"Database insertion failed: {str(e)}")
                            success_count = 0 # If the bulk insert fails, they all fail
                            
                if success_count > 0:
                    messages.success(request, f"Successfully imported {success_count} faculty members.")
                
                if errors:
                    # Display up to 10 errors to avoid overwhelming the screen
                    for err in errors[:10]:
                        messages.warning(request, err)
                    if len(errors) > 10:
                        messages.warning(request, f"...and {len(errors) - 10} more errors.")
                        
                if not success_count and not errors:
                    messages.warning(request, "The CSV file appeared to be empty.")
                    
                return redirect('..')
            except Exception as e:
                messages.error(request, f"A critical error occurred while processing the files: {str(e)}")
                return redirect('..')

        context = {
            **self.admin_site.each_context(request),
            'title': 'Bulk Upload Faculty',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_view_permission': self.has_view_permission(request),
        }
        return render(request, 'admin/home/facultymember/bulk_upload.html', context)

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
