from django.contrib import admin
from .models import AdmissionStep, AdmissionRequirement, AdmissionFee, AdmissionFAQ, AdmissionDeadline

@admin.register(AdmissionStep)
class AdmissionStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(AdmissionRequirement)
class AdmissionRequirementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order')
    list_filter = ('category',)
    list_editable = ('order',)

@admin.register(AdmissionFee)
class AdmissionFeeAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'admission_fee', 'monthly_fee', 'order')
    list_editable = ('order',)

@admin.register(AdmissionFAQ)
class AdmissionFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

@admin.register(AdmissionDeadline)
class AdmissionDeadlineAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_active')
    list_filter = ('is_active',)
