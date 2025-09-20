# apps/transactions/admin.py
from django.contrib import admin
from .models import Transaction, QRPayment

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'from_account', 'to_account', 'amount', 'status', 'timestamp']
    list_filter = ['status', 'transaction_type', 'payment_method', 'timestamp']
    search_fields = ['transaction_id', 'reference_number']
    readonly_fields = ['transaction_id', 'timestamp']

@admin.register(QRPayment)
class QRPaymentAdmin(admin.ModelAdmin):
    list_display = ['qr_code_id', 'account', 'amount', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']