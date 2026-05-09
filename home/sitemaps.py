from django.contrib import sitemaps
from django.urls import reverse
from .models import NewsArticle, AboutUs
from notice_board2.models import NoticeBoard

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'home:home',
            'home:about_us_view',
            'home:faculty_list',
            'home:principal_message',
            'home:vice_principal_message',
            'contact:contact',
            'notice_board2:list',
            'syllabus:syllabus_list',
            'rules:public_rules_list',
            'yearbook:yearbook_list',
            'gallery:gallery_list',
            'admission:admission_home',
        ]

    def location(self, item):
        return reverse(item)

class NewsArticleSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return NewsArticle.objects.all()

    def lastmod(self, obj):
        return obj.published_date

class NoticeBoardSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return NoticeBoard.objects.all()

    def lastmod(self, obj):
        return obj.created_at