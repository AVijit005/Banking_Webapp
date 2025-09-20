# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, BankAccount, Branch, AuditLog

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_verified']
    list_filter = ['role', 'is_verified', 'kyc_verified', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'date_of_birth', 'is_verified', 'kyc_verified')}),
    )

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'account_type', 'balance', 'status']
    list_filter = ['account_type', 'status', 'branch']
    search_fields = ['account_number', 'user__username', 'user__email']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['branch_id', 'name', 'city', 'state', 'manager']
    search_fields = ['name', 'city', 'branch_id']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'timestamp']
    list_filter = ['model_name', 'timestamp']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'changes', 'timestamp']