from django.urls import path
from . import views

app_name = 'debug'

urlpatterns = [
    path('', views.debug_view, name='debug_view'),
]
