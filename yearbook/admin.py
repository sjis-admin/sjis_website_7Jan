from django.contrib import admin
from .models import YearbookEdition, YearbookSection, YearbookPhoto, YearbookMessage, YearbookQuote


class YearbookSectionInline(admin.TabularInline):
    model = YearbookSection
    extra = 1
    fields = ('title', 'description', 'icon', 'order')


class YearbookMessageInline(admin.TabularInline):
    model = YearbookMessage
    extra = 1
    fields = ('author', 'position', 'message', 'photo', 'order')


class YearbookQuoteInline(admin.TabularInline):
    model = YearbookQuote
    extra = 1
    fields = ('student_name', 'student_class', 'quote', 'is_featured')


@admin.register(YearbookEdition)
class YearbookEditionAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'academic_year', 'is_published', 'published_date', 'created_at')
    list_filter = ('is_published', 'year')
    search_fields = ('title', 'year', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [YearbookMessageInline, YearbookSectionInline, YearbookQuoteInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('year', 'title', 'description', 'cover_image')
        }),
        ('Publication', {
            'fields': ('is_published', 'published_date', 'pdf_file')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class YearbookPhotoInline(admin.TabularInline):
    model = YearbookPhoto
    extra = 3
    fields = ('image', 'caption', 'student_name', 'student_class', 'order')


@admin.register(YearbookSection)
class YearbookSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'yearbook', 'order', 'photo_count')
    list_filter = ('yearbook',)
    search_fields = ('title', 'description')
    inlines = [YearbookPhotoInline]
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'


@admin.register(YearbookPhoto)
class YearbookPhotoAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'section', 'student_class', 'order', 'uploaded_at')
    list_filter = ('section__yearbook', 'section', 'student_class')
    search_fields = ('student_name', 'caption', 'student_class')
    readonly_fields = ('uploaded_at',)


@admin.register(YearbookMessage)
class YearbookMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'position', 'yearbook', 'order')
    list_filter = ('yearbook', 'position')
    search_fields = ('author', 'position', 'message')


@admin.register(YearbookQuote)
class YearbookQuoteAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_class', 'yearbook', 'is_featured')
    list_filter = ('yearbook', 'is_featured', 'student_class')
    search_fields = ('student_name', 'quote')
