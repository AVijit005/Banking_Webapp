from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.LoanListView.as_view(), name='loans'),
    path('apply/', views.LoanApplyView.as_view(), name='loan_apply'),
]
