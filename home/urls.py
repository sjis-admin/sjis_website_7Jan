from django.urls import path
from . import views
from .views import faculty_list, about_us_view, principal_message_view, privacy_policy, terms_of_service, sitemap
from django.contrib.sitemaps.views import sitemap as sitemap_view
from home.sitemaps import StaticViewSitemap, NewsArticleSitemap, NewsTickerSitemap

app_name = 'home'

sitemaps = {
    'static': StaticViewSitemap,
    'news': NewsArticleSitemap,
    'news_ticker': NewsTickerSitemap,
}

urlpatterns = [
    path("", views.home, name="home"),
    # path('about/', views.about_us_detail, name='about_us_detail'),
    path('about/', about_us_view, name='about_us_view'),
    path('news/', views.news_list, name='news_list'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('news-ticker/', views.news_ticker, name='news_ticker'),
    path('news-ticker/<int:pk>/', views.news_ticker_details, name='news_ticker_details'),
    path('faculty/', faculty_list, name='faculty_list'),
    path('principal-message/', principal_message_view, name='principal_message'),
    path('vice-principal-message/', views.vice_principal_message_view, name='vice_principal_message'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
    path('sitemap/', sitemap, name='sitemap'),
    path('sitemap.xml', sitemap_view, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]


