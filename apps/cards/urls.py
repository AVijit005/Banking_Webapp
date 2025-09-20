from django.urls import path
from . import views

urlpatterns = [
    path('', views.CardListView.as_view(), name='cards'),
    path('apply/', views.CardApplyView.as_view(), name='card_apply'),
]
