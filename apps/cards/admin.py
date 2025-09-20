# apps/cards/admin.py
from django.contrib import admin
from .models import Card, CardTransaction

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'user', 'card_type', 'status', 'expiry_date']
    list_filter = ['card_type', 'status']
    search_fields = ['card_number', 'user__username']

@admin.register(CardTransaction)
class CardTransactionAdmin(admin.ModelAdmin):
    list_display = ['card', 'amount', 'merchant_name', 'transaction_date']
    list_filter = ['transaction_date']