from django.shortcuts import render
from .models import AdmissionStep, AdmissionRequirement, AdmissionFee, AdmissionFAQ, AdmissionDeadline

def admission_home(request):
    steps = AdmissionStep.objects.all()
    requirements = AdmissionRequirement.objects.all()
    fees = AdmissionFee.objects.all()
    faqs = AdmissionFAQ.objects.all()
    deadlines = AdmissionDeadline.objects.filter(is_active=True)
    
    # Group requirements by category for easy template rendering
    requirements_by_category = []
    for cat_code, cat_name in AdmissionRequirement.CATEGORY_CHOICES:
        cat_reqs = requirements.filter(category=cat_code)
        if cat_reqs.exists():
            requirements_by_category.append({
                'name': cat_name,
                'items': cat_reqs
            })
    
    context = {
        'steps': steps,
        'requirements_by_category': requirements_by_category,
        'fees': fees,
        'faqs': faqs,
        'deadlines': deadlines,
    }
    return render(request, 'admission/admission_home.html', context)
