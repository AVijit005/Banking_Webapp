# fix_urls.py
import os

# Define URL contents for each app
url_contents = {
    'apps/loans/urls.py': '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoanListView.as_view(), name='loans'),
    path('apply/', views.LoanApplyView.as_view(), name='loan_apply'),
]
''',
    'apps/cards/urls.py': '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.CardListView.as_view(), name='cards'),
    path('apply/', views.CardApplyView.as_view(), name='card_apply'),
]
''',
    'apps/insurance/urls.py': '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.InsuranceListView.as_view(), name='insurance'),
    path('apply/', views.InsuranceApplyView.as_view(), name='insurance_apply'),
]
''',
    'apps/accounts/urls.py': '''from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('accounts/', views.AccountListView.as_view(), name='accounts'),
    path('account/<str:account_number>/', views.AccountDetailView.as_view(), name='account_detail'),
]
''',
    'apps/transactions/urls.py': '''from django.urls import path
from . import views

urlpatterns = [
    path('transfer/', views.money_transfer_view, name='money_transfer'),
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('transaction/<uuid:transaction_id>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('qr-payment/', views.QRPaymentView.as_view(), name='qr_payment'),
    path('qr-payments/', views.QRPaymentView.as_view(), name='qr_payments'),
    path('qr-generate/', views.generate_qr_code, name='qr_generate'),
]
''',
    'apps/core/urls.py': '''from django.urls import path
from apps.accounts.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('rewards/', DashboardView.as_view(), name='rewards'),
]
'''
}

# Write all files
for filepath, content in url_contents.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created {filepath}")

print("All URL files created successfully!")