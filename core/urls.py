
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

admin.site.site_header = "St. Joseph International School"
admin.site.site_title = "SJIS Admin Portal"
admin.site.index_title = "Welcome to SJIS Portal"

urlpatterns =[
    path('admin/', admin.site.urls),
    path('robots.txt', RedirectView.as_view(url="/static/robots.txt", permanent=True)),
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

    

