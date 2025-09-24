from django.urls import path
from . import views

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Dashboard URL removed - handled by core app to avoid conflicts
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('accounts/', views.AccountListView.as_view(), name='account_list'),
    path('account/<str:account_number>/', views.AccountDetailView.as_view(), name='account_detail'),
]
