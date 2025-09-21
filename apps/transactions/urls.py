from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('<uuid:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('transfer/', views.money_transfer, name='money_transfer'),
    path('qr/generate/', views.qr_generate, name='qr_generate'),
    path('qr/<uuid:qr_id>/', views.qr_payment, name='qr_payment'),
    path('qr/scan/', views.qr_scan, name='qr_scan'),
    path('qr/process/', views.process_qr_payment, name='process_qr_payment'),
]
