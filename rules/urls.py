from django.urls import path
from . import views

app_name = 'rules'

urlpatterns = [
    # Public-facing URLs (no login required)
    path('', views.public_rules_list, name='public_rules_list'),
    path('category/<int:category_id>/', views.public_category_view, name='public_category_view'),
    path('rule/<int:rule_id>/', views.public_rule_detail, name='public_rule_detail'),
    
    # Admin/Staff URLs (login required)
    path('dashboard/', views.rule_dashboard, name='rule_dashboard'),
    path('admin/categories/', views.rule_category_list, name='rule_category_list'),
    path('admin/rules/', views.rule_list, name='rule_list'),
    path('admin/rules/category/<int:category_id>/', views.rule_list, name='rules_by_category'),
    path('admin/rules/<int:rule_id>/', views.rule_detail, name='rule_detail'),
    path('admin/rules/<int:rule_id>/report/', views.report_violation, name='report_violation'),
]