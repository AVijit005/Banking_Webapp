from django.db import models
from django.contrib.auth import get_user_model
from apps.accounts.models import BankAccount
import uuid

User = get_user_model()

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('payment', 'Payment'),
        ('interest', 'Interest Credit'),
        ('fee', 'Service Fee'),
    ]
    
    TRANSACTION_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('online', 'Online Transfer'),
        ('qr', 'QR Payment'),
        ('card', 'Card Payment'),
    ]
    
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    from_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, 
                                   related_name='sent_transactions', null=True, blank=True)
    to_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, 
                                 related_name='received_transactions', null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True)
    reference_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    initiated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                   related_name='approved_transactions', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type} - ${self.amount}"

class QRPayment(models.Model):
    qr_code_id = models.UUIDField(default=uuid.uuid4, unique=True)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purpose = models.CharField(max_length=200)
    qr_code_image = models.ImageField(upload_to='qr_codes/')
    is_active = models.BooleanField(default=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'qr_payments'
