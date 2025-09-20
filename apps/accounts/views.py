# apps/accounts/views.py
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'

class AccountListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    
    def get_queryset(self):
        return []  # Will be implemented later

class AccountDetailView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/account_detail.html'
    
    def get_object(self):
        return None  # Will be implemented later