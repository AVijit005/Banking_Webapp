from django.db import models
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
