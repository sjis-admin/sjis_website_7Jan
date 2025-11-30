from django.shortcuts import render, get_object_or_404
from .models import YearbookEdition, YearbookSection, YearbookPhoto


def yearbook_list(request):
    """List all published yearbooks"""
    yearbooks = YearbookEdition.objects.filter(is_published=True).prefetch_related('messages', 'quotes')
    
    context = {
        'yearbooks': yearbooks,
    }
    
    return render(request, 'yearbook/yearbook_list.html', context)


def yearbook_detail(request, year):
    """View specific yearbook with all sections"""
    yearbook = get_object_or_404(
        YearbookEdition.objects.prefetch_related('sections__photos', 'messages', 'quotes'),
        year=year,
        is_published=True
    )
    
    sections = yearbook.sections.all()
    messages = yearbook.messages.all()
    featured_quotes = yearbook.quotes.filter(is_featured=True)
    
    context = {
        'yearbook': yearbook,
        'sections': sections,
        'messages': messages,
        'featured_quotes': featured_quotes,
    }
    
    return render(request, 'yearbook/yearbook_detail.html', context)


def yearbook_gallery(request, year, section_id):
    """Photo gallery view for a specific section"""
    yearbook = get_object_or_404(YearbookEdition, year=year, is_published=True)
    section = get_object_or_404(YearbookSection, id=section_id, yearbook=yearbook)
    photos = section.photos.all()
    
    context = {
        'yearbook': yearbook,
        'section': section,
        'photos': photos,
    }
    
    return render(request, 'yearbook/yearbook_gallery.html', context)
