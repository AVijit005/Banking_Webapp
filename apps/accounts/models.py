from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='USA')
    postal_code = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    kyc_verified = models.BooleanField(default=False)
    kyc_documents = models.JSONField(default=dict, blank=True)
    preferred_language = models.CharField(max_length=10, default='en')
    theme_preference = models.CharField(max_length=10, default='light')
    two_factor_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

class Branch(models.Model):
    branch_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               related_name='managed_branches')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'branches'
        verbose_name_plural = 'Branches'
    
    def __str__(self):
        return f"{self.name} ({self.branch_id})"

class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('savings', 'Savings Account'),
        ('current', 'Current Account'),
        ('business', 'Business Account'),
        ('salary', 'Salary Account'),
        ('fixed_deposit', 'Fixed Deposit'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('frozen', 'Frozen'),
        ('closed', 'Closed'),
    ]
    
    account_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    minimum_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    opened_date = models.DateTimeField(auto_now_add=True)
    last_transaction_date = models.DateTimeField(null=True, blank=True)
    daily_withdrawal_limit = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00)
    
    class Meta:
        db_table = 'bank_accounts'
    
    def __str__(self):
        return f"{self.account_number} - {self.user.get_full_name()}"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=200)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
