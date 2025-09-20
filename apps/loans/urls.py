from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoanListView.as_view(), name='loans'),
    path('apply/', views.LoanApplyView.as_view(), name='loan_apply'),
]
