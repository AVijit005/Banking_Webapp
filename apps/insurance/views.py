# apps/insurance/views.py
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class InsuranceListView(LoginRequiredMixin, ListView):
    template_name = 'insurance/insurance_list.html'
    context_object_name = 'policies'
    
    def get_queryset(self):
        return []

class InsuranceApplyView(LoginRequiredMixin, TemplateView):
    template_name = 'insurance/insurance_apply.html'