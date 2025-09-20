from django.urls import path
from apps.accounts.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('rewards/', DashboardView.as_view(), name='rewards'),
]
