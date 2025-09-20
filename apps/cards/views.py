# apps/cards/views.py
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class CardListView(LoginRequiredMixin, ListView):
    template_name = 'cards/card_list.html'
    context_object_name = 'cards'
    
    def get_queryset(self):
        return []

class CardApplyView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/card_apply.html'