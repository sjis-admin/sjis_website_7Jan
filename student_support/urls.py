from django.urls import path
from . import views

app_name = 'student_support'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('appointment/', views.appointment_request_view, name='appointment_request'),
    path('resources/', views.resource_list_view, name='resource_list'),
]
