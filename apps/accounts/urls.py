from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('accounts/', views.AccountListView.as_view(), name='accounts'),
    path('account/<str:account_number>/', views.AccountDetailView.as_view(), name='account_detail'),
]
