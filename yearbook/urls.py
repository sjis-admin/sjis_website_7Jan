from django.urls import path
from . import views

app_name = 'yearbook'

urlpatterns = [
    path('', views.yearbook_list, name='yearbook_list'),
]
