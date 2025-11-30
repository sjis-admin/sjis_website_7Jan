from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, FAQ, Counselor, SupportResource
from .forms import AppointmentRequestForm

def home_view(request):
    services = Service.objects.all()
    faqs = FAQ.objects.all()
    counselors = Counselor.objects.all()
    recent_resources = SupportResource.objects.all().order_by('-uploaded_at')[:3]
    
    context = {
        'services': services,
        'faqs': faqs,
        'counselors': counselors,
        'recent_resources': recent_resources
    }
    return render(request, 'student_support/support_base.html', context)


def contact_view(request):
    return render(request, 'student_support/contact.html')

def appointment_request_view(request):
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your appointment request has been submitted successfully. We will contact you shortly.')
            return redirect('student_support:home')
    else:
        form = AppointmentRequestForm()
    
    return render(request, 'student_support/appointment_form.html', {'form': form})

def resource_list_view(request):
    resources = SupportResource.objects.all()
    category = request.GET.get('category')
    
    if category:
        resources = resources.filter(category=category)
        
    context = {
        'resources': resources,
        'categories': SupportResource.CATEGORY_CHOICES,
        'selected_category': category
    }
    return render(request, 'student_support/resource_list.html', context)
