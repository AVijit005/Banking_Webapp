from django.urls import path
from . import views

app_name = 'insurance'

urlpatterns = [
    path('', views.InsuranceListView.as_view(), name='insurance'),
    path('apply/', views.InsuranceApplyView.as_view(), name='insurance_apply'),
]
