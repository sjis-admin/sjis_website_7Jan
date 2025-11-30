"""
URL configuration for chatbot app.
"""
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('api/chat/', views.chat_message, name='chat_message'),
    path('api/context/', views.get_context, name='get_context'),
]
