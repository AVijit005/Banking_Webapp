from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.utils import timezone
from .forms import LoginForm, UserRegistrationForm
import json

User = get_user_model()

class DashboardView(TemplateView):
    """Main dashboard view that redirects based on user role"""
    template_name = 'dashboard/dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Add basic context
        context['user'] = user
        context['title'] = 'Dashboard - Banking System'
        context['total_balance'] = 0.00
        context['recent_transactions'] = []
        context['accounts'] = []
        
        # Add role-specific context with error handling
        try:
            if hasattr(user, 'role') and user.role:
                if user.role == 'customer':
                    context.update(self.get_customer_context(user))
                elif user.role == 'employee':
                    context.update(self.get_employee_context(user))
                elif user.role == 'manager':
                    context.update(self.get_manager_context(user))
                elif user.role == 'admin':
                    context.update(self.get_admin_context(user))
        except Exception as e:
            # If there's an error, just use basic context
            context['error'] = f"Dashboard error: {str(e)}"
        
        return context
    
    def get_customer_context(self, user):
        """Get context data for customer dashboard"""
        from apps.accounts.models import BankAccount, Rewards, Notification
        from apps.transactions.models import Transaction
        
        accounts = BankAccount.objects.filter(user=user, status='active')
        recent_transactions = Transaction.objects.filter(
            from_account__user=user
        ).order_by('-timestamp')[:5]
        
        try:
            rewards = Rewards.objects.get(user=user)
        except Rewards.DoesNotExist:
            rewards = Rewards.objects.create(user=user)
        
        notifications = Notification.objects.filter(
            user=user, is_read=False
        ).order_by('-created_at')[:5]
        
        return {
            'accounts': accounts,
            'recent_transactions': recent_transactions,
            'rewards': rewards,
            'notifications': notifications,
            'total_balance': sum(account.balance for account in accounts),
        }
    
    def get_employee_context(self, user):
        """Get context data for employee dashboard"""
        from apps.accounts.models import BankAccount, User
        from apps.transactions.models import Transaction
        
        # Get pending approvals
        pending_transactions = Transaction.objects.filter(
            status='pending'
        ).order_by('-timestamp')[:10]
        
        # Get recent customer registrations
        recent_customers = User.objects.filter(
            role='customer'
        ).order_by('-date_joined')[:5]
        
        return {
            'pending_transactions': pending_transactions,
            'recent_customers': recent_customers,
        }
    
    def get_manager_context(self, user):
        """Get context data for manager dashboard"""
        from apps.accounts.models import BankAccount, User
        from apps.transactions.models import Transaction
        from apps.loans.models import Loan
        from apps.insurance.models import Insurance
        
        # Get pending approvals
        pending_loans = Loan.objects.filter(status='pending')[:10]
        pending_insurance = Insurance.objects.filter(status='pending')[:10]
        pending_transactions = Transaction.objects.filter(
            status='pending'
        ).order_by('-timestamp')[:10]
        
        return {
            'pending_loans': pending_loans,
            'pending_insurance': pending_insurance,
            'pending_transactions': pending_transactions,
        }
    
    def get_admin_context(self, user):
        """Get context data for admin dashboard"""
        from apps.accounts.models import BankAccount, User, AuditLog
        from apps.transactions.models import Transaction
        
        # System statistics
        total_users = User.objects.count()
        total_accounts = BankAccount.objects.count()
        total_transactions = Transaction.objects.count()
        recent_audit_logs = AuditLog.objects.order_by('-timestamp')[:10]
        
        return {
            'total_users': total_users,
            'total_accounts': total_accounts,
            'total_transactions': total_transactions,
            'recent_audit_logs': recent_audit_logs,
        }

def login_view(request):
    """Enhanced login view with 2FA support"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    
                    # Redirect to dashboard
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'title': 'Login - Banking System'
    }
    return render(request, 'registration/login.html', context)

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Create rewards account
            from apps.accounts.models import Rewards
            Rewards.objects.create(user=user)
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    """User profile management"""
    if request.method == 'POST':
        # Handle profile updates
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)
        user.postal_code = request.POST.get('postal_code', user.postal_code)
        user.theme_preference = request.POST.get('theme_preference', user.theme_preference)
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'accounts/profile.html')

@login_required
def notifications_view(request):
    """Notifications management"""
    from apps.accounts.models import Notification
    
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        action = request.POST.get('action')
        
        if action == 'mark_read':
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
        elif action == 'mark_all_read':
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        
        return JsonResponse({'success': True})
    
    return render(request, 'dashboard/notifications.html', {'notifications': notifications})

@csrf_exempt
def api_health_check(request):
    """API health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
    })
</create_file>
