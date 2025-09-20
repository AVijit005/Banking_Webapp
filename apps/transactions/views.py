# apps/transactions/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required
def money_transfer_view(request):
    return render(request, 'transactions/money_transfer.html')

class TransactionListView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    
    def get_queryset(self):
        return []

class TransactionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'transactions/transaction_detail.html'
    
    def get_object(self):
        return None

class QRPaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions/qr_payment.html'

@login_required
def generate_qr_code(request):
    return render(request, 'transactions/qr_generate.html')