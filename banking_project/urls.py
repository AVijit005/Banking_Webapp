# banking_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),  # This will handle the root URL
    path('accounts/', include('apps.accounts.urls')),
    path('transactions/', include('apps.transactions.urls')),
    path('loans/', include('apps.loans.urls')),
    path('cards/', include('apps.cards.urls')),
    path('insurance/', include('apps.insurance.urls')),
    path('auth/', include('django.contrib.auth.urls')),  # Use Django's built-in auth
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)