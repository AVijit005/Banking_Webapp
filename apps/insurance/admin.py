# apps/insurance/admin.py
from django.contrib import admin
from .models import Insurance, InsuranceClaim

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'user', 'insurance_type', 'status', 'premium_amount']
    list_filter = ['insurance_type', 'status']
    search_fields = ['policy_number', 'user__username']

@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_id', 'policy', 'claim_amount', 'status', 'submitted_date']
    list_filter = ['status', 'submitted_date']