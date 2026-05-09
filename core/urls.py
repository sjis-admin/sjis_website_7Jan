
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap
from home.sitemaps import StaticViewSitemap, NewsArticleSitemap, NoticeBoardSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'news': NewsArticleSitemap,
    'notices': NoticeBoardSitemap,
}

admin.site.site_header = "St. Joseph International School"
admin.site.site_title = "SJIS Admin Portal"
admin.site.index_title = "Welcome to SJIS Portal"

from django.http import HttpResponse

def robots_txt(request):
    content = "User-agent: *\nDisallow: /admin/\nDisallow: /tinymce/\nDisallow: /debug/\nDisallow: /student_support/\n\nHost: https://www.sjis.edu.bd\nSitemap: https://www.sjis.edu.bd/sitemap.xml"
    return HttpResponse(content, content_type="text/plain")

urlpatterns =[
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('', include('home.urls', namespace='home')),
    path('notice-board2/', include('notice_board2.urls', namespace='notice_board2')),
    # path('notice-board2/', include('notice_board2.urls', namespace='notice_board2')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('club_new/', include('club_new.urls', namespace='club_new')),
    path('syllabus/', include('syllabus.urls', namespace='syllabus')),
    path('rules/', include('rules.urls', namespace='rules')),
    path('yearbook/', include('yearbook.urls', namespace='yearbook')),
    path('admission/', include('admission.urls', namespace='admission')),
    path('gallery/', include('gallery.urls', namespace='gallery')),
    path('chatbot/', include('chatbot.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('academic_calendar/', include('academic_calendar.urls', namespace='academic_calendar')),
    path('student_support/', include('student_support.urls', namespace='student_support')),
    path('debug/', include('debug.urls', namespace='debug')),
    
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    

