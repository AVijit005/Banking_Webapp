# setup_models.py
import os

models_content = {
    'apps/accounts/models.py': '''from django.contrib.auth.models import AbstractUser
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
''',

    'apps/transactions/models.py': '''from django.db import models
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
''',

    'apps/loans/models.py': '''from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Loan(models.Model):
    LOAN_TYPES = [
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('auto', 'Auto Loan'),
        ('education', 'Education Loan'),
        ('business', 'Business Loan'),
    ]
    
    LOAN_STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('defaulted', 'Defaulted'),
    ]
    
    loan_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, 
                                      validators=[MinValueValidator(0), MaxValueValidator(100)])
    tenure_months = models.IntegerField(validators=[MinValueValidator(1)])
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_payable = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='pending')
    purpose = models.TextField()
    collateral = models.TextField(blank=True)
    guarantor_name = models.CharField(max_length=200, blank=True)
    guarantor_contact = models.CharField(max_length=20, blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='approved_loans', blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)
    next_emi_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'loans'
''',

    'apps/cards/models.py': '''from django.db import models
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
''',

    'apps/insurance/models.py': '''from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Insurance(models.Model):
    INSURANCE_TYPES = [
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('vehicle', 'Vehicle Insurance'),
        ('property', 'Property Insurance'),
    ]
    
    POLICY_STATUS = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('claim_processing', 'Claim Processing'),
    ]
    
    policy_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insurance_policies')
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium_frequency = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=POLICY_STATUS, default='pending')
    beneficiary_name = models.CharField(max_length=200)
    beneficiary_relationship = models.CharField(max_length=100)
    beneficiary_contact = models.CharField(max_length=20)
    policy_document = models.FileField(upload_to='insurance_documents/', null=True, blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='approved_insurances', blank=True)
    
    class Meta:
        db_table = 'insurance_policies'

class InsuranceClaim(models.Model):
    CLAIM_STATUS = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    
    claim_id = models.CharField(max_length=20, unique=True)
    policy = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='claims')
    claim_amount = models.DecimalField(max_digits=12, decimal_places=2)
    claim_reason = models.TextField()
    incident_date = models.DateField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CLAIM_STATUS, default='submitted')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='reviewed_claims', blank=True)
    review_notes = models.TextField(blank=True)
    supporting_documents = models.JSONField(default=list)
    
    class Meta:
        db_table = 'insurance_claims'
'''
}

# Write all model files
for filepath, content in models_content.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {filepath}")

print("All model files created successfully!")