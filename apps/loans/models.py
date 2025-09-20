from django.db import models
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
