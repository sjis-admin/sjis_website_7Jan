from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'notice_board2'  # Namespace for the notice board app
urlpatterns = [
    # Default notice board view
    path('', views.NoticeBoardListView.as_view(), name='list'),
    
    # Detail view - accessible to all
    path('notice/<int:pk>/', views.NoticeBoardDetailView.as_view(), name='detail'),
    
    # Create view - requires login
    path('create/', 
         login_required(views.NoticeBoardCreateView.as_view()), 
         name='create'),
    
    # Update view - requires login and specific permissions
    path('update/<int:pk>/', 
         login_required(views.NoticeBoardUpdateView.as_view()), 
         name='update'),
    
    # Delete view - requires login and specific permissions
    path('delete/<int:pk>/', 
         login_required(views.NoticeBoardDeleteView.as_view()), 
         name='delete'),
    
    # Optional: Filtered list views
    path('grade/<str:grade>/', 
         views.NoticeBoardListView.as_view(), 
         name='grade_filter'),
]

# from django.urls import path
# from django.contrib.auth.decorators import login_required
# from . import views

# app_name = 'notice_board2'  # Namespace for the notice board app

# urlpatterns = [
#     # Default notice board view with pagination
#     path('', views.notice_board, name='notice_board'),
    
#     # List view - accessible to all
#     path('list/', views.NoticeBoardListView.as_view(), name='list'),
    
#     # Detail view - accessible to all
#     path('notice/<int:pk>/', views.NoticeBoardDetailView.as_view(), name='detail'),
    
#     # Create view - requires login
#     path('create/', 
#          login_required(views.NoticeBoardCreateView.as_view()), 
#          name='create'),
    
#     # Update view - requires login and specific permissions
#     path('update/<int:pk>/', 
#          login_required(views.NoticeBoardUpdateView.as_view()), 
#          name='update'),
    
#     # Delete view - requires login and specific permissions
#     path('delete/<int:pk>/', 
#          login_required(views.NoticeBoardDeleteView.as_view()), 
#          name='delete'),
    
#     # Optional: Filtered list views
#     path('grade/<str:grade>/', 
#          views.NoticeBoardListView.as_view(), 
#          name='grade_filter'),
# ]

