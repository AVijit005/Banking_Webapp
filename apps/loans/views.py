# apps/loans/views.py
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanListView(LoginRequiredMixin, ListView):
    template_name = 'loans/loan_list.html'
    context_object_name = 'loans'
    
    def get_queryset(self):
        return []

class LoanApplyView(LoginRequiredMixin, TemplateView):
    template_name = 'loans/loan_apply.html'