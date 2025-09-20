from django.urls import path
from . import views

urlpatterns = [
    path('transfer/', views.money_transfer_view, name='money_transfer'),
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('transaction/<uuid:transaction_id>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('qr-payment/', views.QRPaymentView.as_view(), name='qr_payment'),
    path('qr-payments/', views.QRPaymentView.as_view(), name='qr_payments'),
    path('qr-generate/', views.generate_qr_code, name='qr_generate'),
]
