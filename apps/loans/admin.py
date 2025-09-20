# apps/loans/admin.py
from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['loan_id', 'user', 'loan_type', 'principal_amount', 'status']
    list_filter = ['loan_type', 'status']
    search_fields = ['loan_id', 'user__username']