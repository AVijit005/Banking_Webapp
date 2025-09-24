# apps/accounts/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404
from django.db import models
from .models import BankAccount

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)
        user.postal_code = request.POST.get('postal_code', user.postal_code)
        user.theme_preference = request.POST.get('theme_preference', user.theme_preference)
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'

class AccountListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        """Return user's active bank accounts"""
        return BankAccount.objects.filter(
            user=self.request.user,
            status='active'
        ).order_by('-opened_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_balance'] = sum(account.balance for account in context['accounts'])
        context['account_types'] = BankAccount.ACCOUNT_TYPES
        return context

class AccountDetailView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/account_detail.html'
    context_object_name = 'account'

    def get_object(self):
        """Get specific account by account number"""
        account_number = self.kwargs.get('account_number')
        try:
            return BankAccount.objects.get(
                account_number=account_number,
                user=self.request.user
            )
        except BankAccount.DoesNotExist:
            raise Http404("Account not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = context['account']

        # Get recent transactions for this account
        from apps.transactions.models import Transaction
        context['recent_transactions'] = Transaction.objects.filter(
            models.Q(from_account=account) | models.Q(to_account=account)
        ).order_by('-timestamp')[:10]

        context['can_withdraw'] = account.balance > account.minimum_balance
        return context
