from django.shortcuts import render, get_object_or_404
from .models import YearbookEdition

def yearbook_list(request):
    """List all published yearbooks for PDF viewing"""
    yearbooks = YearbookEdition.objects.filter(is_published=True)
    
    context = {
        'yearbooks': yearbooks,
    }
    
    return render(request, 'yearbook/yearbook_list.html', context)
