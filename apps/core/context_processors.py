# apps/core/context_processors.py
def theme_context(request):
    """Add theme-related context to all templates"""
    theme = 'light'
    if request.user.is_authenticated:
        theme = getattr(request.user, 'theme_preference', 'light')
    
    return {
        'theme': theme,
        'app_name': 'SecureBank',
        'support_email': 'support@securebank.com',
        'support_phone': '+1-800-SECURE-BANK',
    }