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
    
    # Leadership Messages
    principal_msg = PrincipalMessage.objects.filter(is_active=True, type='Principal').first()
    vp_msg = PrincipalMessage.objects.filter(is_active=True, type='VicePrincipal').first()
    
    context = {
        'images': images,
        'image_count': images.count(),
        'about_us': about_us,
        'news_articles': news_articles,
        'news_items': news_items,
        'notices': notices,
        'principal_msg': principal_msg,
        'vp_msg': vp_msg,
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
    active_tab = request.GET.get('tab', 'Administration')
    search_query = request.GET.get('q', '').strip()

    # Smart hierarchy ranking: Principal #1, Vice-Principal #2, Heads #3, others #99
    hierarchy_rank = Case(
        When(designation__iexact='Principal', then=Value(1)),
        When(designation__icontains='Principal', then=Value(2)),
        When(designation__icontains='Vice', then=Value(3)),
        When(designation__icontains='Head', then=Value(4)),
        default=Value(99),
        output_field=IntegerField()
    )

    # Base queryset with hierarchy ordering
    queryset = FacultyMember.objects.all().only(
        'id', 'name', 'designation', 'category', 'image', 'order'
    ).annotate(rank=hierarchy_rank)

    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(designation__icontains=search_query)
        )

    categories = {
        "Administration": queryset.filter(category="Administration").order_by('order', 'rank', 'id'),
        "Teachers": queryset.filter(category="Teacher").order_by('order', 'rank', 'id'),
        "Office Staff": queryset.filter(category="Office Staff").order_by('order', 'rank', 'id'),
    }

    items_per_page = 12
    paginated_categories = {}

    for category, members in categories.items():
        if category == active_tab:
            paginator = Paginator(members, items_per_page)
            page_number = request.GET.get('page', 1)
            paginated_categories[category] = paginator.get_page(page_number)
        else:
            # Lazy lightweight stub containing count for inactive tabs without evaluating queryset
            class LazyPageStub:
                def __init__(self, count):
                    self.paginator = type('PaginatorStub', (), {'count': count})()
                    self.object_list = []
            paginated_categories[category] = LazyPageStub(members.count())

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

