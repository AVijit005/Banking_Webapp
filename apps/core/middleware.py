# apps/core/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime, timedelta
from django.conf import settings

class SessionTimeoutMiddleware(MiddlewareMixin):
    """Logout users after inactivity period"""
    
    def process_request(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            
            if last_activity:
                last_activity = datetime.fromisoformat(last_activity)
                if datetime.now() - last_activity > timedelta(minutes=30):
                    logout(request)
                    return redirect(reverse('login') + '?timeout=1')
            
            request.session['last_activity'] = datetime.now().isoformat()


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses"""
    
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response