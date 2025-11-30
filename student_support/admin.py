from django.contrib import admin
from .models import Service, FAQ, Counselor, SupportResource, AppointmentRequest

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')
    search_fields = ('title',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
    search_fields = ('question',)

@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email')
    search_fields = ('name', 'role', 'email')
    list_filter = ('role',)

@admin.register(SupportResource)
class SupportResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'email', 'counselor', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'counselor', 'preferred_date')
    search_fields = ('student_name', 'email', 'student_id')
    readonly_fields = ('created_at',)
