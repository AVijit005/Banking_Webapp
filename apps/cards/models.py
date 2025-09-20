from django.db import models
from django.contrib.auth import get_user_model
from apps.accounts.models import BankAccount
import random

User = get_user_model()

class Card(models.Model):
    CARD_TYPES = [
        ('debit', 'Debit Card'),
        ('credit', 'Credit Card'),
    ]
    
    CARD_STATUS = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('expired', 'Expired'),
        ('pending', 'Pending Activation'),
    ]
    
    card_number = models.CharField(max_length=16, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, 
                              related_name='linked_cards', null=True, blank=True)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    card_holder_name = models.CharField(max_length=100)
    cvv = models.CharField(max_length=3)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=CARD_STATUS, default='pending')
    issued_date = models.DateTimeField(auto_now_add=True)
    daily_limit = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00)
    international_usage = models.BooleanField(default=False)
    online_usage = models.BooleanField(default=True)
    contactless_enabled = models.BooleanField(default=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minimum_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    billing_cycle_day = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'cards'

class CardTransaction(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant_name = models.CharField(max_length=200)
    merchant_category = models.CharField(max_length=100)
    transaction_date = models.DateTimeField(auto_now_add=True)
    authorization_code = models.CharField(max_length=20)
    is_international = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'card_transactions'
        ordering = ['-transaction_date']
