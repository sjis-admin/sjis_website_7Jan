from django.urls import path
from . import views

app_name = 'yearbook'

urlpatterns = [
    path('', views.yearbook_list, name='yearbook_list'),
    path('<int:year>/gallery/<int:section_id>/', views.yearbook_gallery, name='yearbook_gallery'),
]
