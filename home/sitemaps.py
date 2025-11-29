# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import NewsArticle, NewsTicker, FacultyMember, AboutUs

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home:home', 'home:about_us_view', 'home:faculty_list', 
                'home:principal_message', 'home:vice_principal_message']

    def location(self, item):
        return reverse(item)

class NewsArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return NewsArticle.objects.all()

    def lastmod(self, obj):
        return obj.published_date

    def location(self, obj):
        return reverse('home:news_detail', args=[obj.pk])

class NewsTickerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return NewsTicker.objects.all()

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        return reverse('home:news_ticker_details', args=[obj.pk])