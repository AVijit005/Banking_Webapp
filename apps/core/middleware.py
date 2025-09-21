import time
import json
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()

class AuditLogMiddleware(MiddlewareMixin):
    """Middleware to log user actions for audit purposes"""
    
    def process_request(self, request):
        request.audit_start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'audit_start_time') and request.user.is_authenticated:
            duration = time.time() - request.audit_start_time
            
            # Log significant actions (commented out for now)
            # if request.method in ['POST', 'PUT', 'DELETE'] and response.status_code < 400:
            #     from apps.accounts.models import AuditLog
            #     AuditLog.objects.create(
            #         user=request.user,
            #         action=f"{request.method} {request.path}",
            #         model_name=request.path.split('/')[1] if len(request.path.split('/')) > 1 else 'unknown',
            #         ip_address=self.get_client_ip(request),
            #         user_agent=request.META.get('HTTP_USER_AGENT', ''),
            #     )
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RateLimitMiddleware(MiddlewareMixin):
    """Middleware to implement rate limiting"""
    
    def process_request(self, request):
        # Skip rate limiting for certain paths
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return None
        
        # Get client IP
        ip = self.get_client_ip(request)
        
        # Rate limiting rules
        if request.path.startswith('/auth/login/'):
            limit = 5  # 5 login attempts per minute
            window = 60
        elif request.path.startswith('/api/'):
            limit = 100  # 100 API calls per minute
            window = 60
        else:
            limit = 200  # 200 page requests per minute
            window = 60
        
        # Check rate limit
        cache_key = f"rate_limit_{ip}_{request.path}"
        current_requests = cache.get(cache_key, 0)
        
        if current_requests >= limit:
            return JsonResponse({
                'error': 'Rate limit exceeded. Please try again later.',
                'retry_after': window
            }, status=429)
        
        # Increment counter
        cache.set(cache_key, current_requests + 1, window)
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip