from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'core'

def root_redirect(request):
    """Redirect root URL to login page"""
    return redirect('login')

urlpatterns = [
    # Root URL - redirect to login
    path('', root_redirect, name='root'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/budgeting/', views.BudgetingView.as_view(), name='budgeting'),
    
    # Profile & Settings
    path('notifications/', views.notifications_view, name='notifications'),
    
    # API Endpoints
    path('api/health/', views.api_health_check, name='api_health_check'),
]
