from django.urls import path
from . import views

app_name = 'admission'

urlpatterns = [
    path('', views.admission_home, name='admission_home'),
]
