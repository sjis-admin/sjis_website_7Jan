# home/views.py
from django.shortcuts import render, get_object_or_404
from .models import CarouselImage, AboutUs, NewsArticle, NewsTicker, FacultyMember, PrincipalMessage
from notice_board2.models import NoticeBoard  # Changed from Notice
from .models import AboutUs
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

def home(request):
    images = CarouselImage.objects.filter(is_active=True)
    about_us = AboutUs.objects.first()
    news_articles = NewsArticle.objects.all().order_by('-published_date')[:4]
    news_items = NewsTicker.objects.all()
    notices = NoticeBoard.objects.all().order_by('-created_at')[:5]
    
    context = {
        'images': images,
        'image_count': images.count(),
        'about_us': about_us,
        'news_articles': news_articles,
        'news_items': news_items,
        'notices': notices,
    }
    return render(request, 'home/home.html', context)






def news_list(request):
    news_articles = NewsArticle.objects.all().order_by('-published_date')
    return render(request, 'home/news_archive.html', {'news_articles': news_articles})

def news_detail(request, pk):
    news_article = get_object_or_404(NewsArticle, pk=pk)
    latest_news = NewsArticle.objects.exclude(pk=pk).order_by('-published_date')[:5]
    return render(request, 'home/news_detail.html', {'news_article': news_article, 'latest_news': latest_news})

def news_ticker(request):
    news_items = NewsTicker.objects.all()
    return render(request, 'home/news_ticker.html', {'news_items': news_items})

def news_ticker_details(request, pk):
    news_item = get_object_or_404(NewsTicker, pk=pk)
    return render(request, 'home/news_ticker_details.html', {'news_item': news_item})




def faculty_list(request):
    # Determine the active tab, default to 'Administration'
    active_tab = request.GET.get('tab', 'Administration')
    search_query = request.GET.get('q', '')

    # Base queryset
    queryset = FacultyMember.objects.all()

    # Apply search filter if query exists
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(designation__icontains=search_query)
        )

    # Define the categories and their corresponding filters
    # We filter the already searched queryset by category
    categories = {
        "Administration": queryset.filter(category="Administration"),
        "Teachers": queryset.filter(category="Teacher"),
        "Office Staff": queryset.filter(category="Office Staff"),
    }

    items_per_page = 12  # Reduced for better grid layout
    paginated_categories = {}

    for category, members in categories.items():
        paginator = Paginator(members, items_per_page)
        
        # Paginate only the active tab
        if category == active_tab:
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            # For all other tabs, just show the first page
            page_obj = paginator.get_page(1)
            
        paginated_categories[category] = page_obj

    context = {
        "categories": paginated_categories,
        "active_tab": active_tab,
        "items_per_page": items_per_page,
        "search_query": search_query,
    }

    return render(request, "home/faculty_list.html", context)


def about_us_view(request):
    about_us = AboutUs.objects.first()  # Fetch the first AboutUs instance
    if about_us:
        sections = about_us.sections.all()
    else:
        sections = []
    
    context = {
        'about_us': about_us,
        'sections': sections
    }
    
    return render(request, 'home/about_us.html', context)
    


def principal_message_view(request):
    message = PrincipalMessage.objects.filter(is_active=True, type='Principal').first()
    return render(request, 'home/message.html', {'message': message, 'role': 'Principal'})

def vice_principal_message_view(request):
    message = PrincipalMessage.objects.filter(is_active=True, type='VicePrincipal').first()
    return render(request, 'home/message.html', {'message': message, 'role': 'Vice-Principal'})

def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'home/terms_of_service.html')

def sitemap(request):
    return render(request, 'home/sitemap.html')

