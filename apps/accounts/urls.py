from django.urls import path
from . import views

urlpatterns = [
    # Dashboard URL removed - handled by core app to avoid conflicts
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('accounts/', views.AccountListView.as_view(), name='accounts'),
    path('account/<str:account_number>/', views.AccountDetailView.as_view(), name='account_detail'),
]
