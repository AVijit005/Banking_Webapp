# setup_templates.py
import os

# Create directories
directories = [
    'templates/accounts',
    'templates/loans',
    'templates/cards',
    'templates/insurance',
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

# Template contents
templates = {
    'templates/accounts/profile.html': '''{% extends 'base.html' %}
{% block title %}Profile - SecureBank{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">My Profile</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Profile page coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/accounts/settings.html': '''{% extends 'base.html' %}
{% block title %}Settings - SecureBank{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">Settings</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Settings page coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/accounts/account_list.html': '''{% extends 'base.html' %}
{% block title %}My Accounts - SecureBank{% endblock %}
{% block content %}
<div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">My Accounts</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Account list coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/accounts/account_detail.html': '''{% extends 'base.html' %}
{% block title %}Account Details - SecureBank{% endblock %}
{% block content %}
<div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">Account Details</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Account details coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/loans/loan_list.html': '''{% extends 'base.html' %}
{% block title %}My Loans - SecureBank{% endblock %}
{% block content %}
<div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">My Loans</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Loan list coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/loans/loan_apply.html': '''{% extends 'base.html' %}
{% block title %}Apply for Loan - SecureBank{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">Apply for Loan</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Loan application form coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/cards/card_list.html': '''{% extends 'base.html' %}
{% block title %}My Cards - SecureBank{% endblock %}
{% block content %}
<div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">My Cards</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Card list coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/cards/card_apply.html': '''{% extends 'base.html' %}
{% block title %}Apply for Card - SecureBank{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">Apply for Card</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Card application form coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/insurance/insurance_list.html': '''{% extends 'base.html' %}
{% block title %}My Insurance - SecureBank{% endblock %}
{% block content %}
<div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">My Insurance Policies</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Insurance list coming soon...</p>
    </div>
</div>
{% endblock %}''',

    'templates/insurance/insurance_apply.html': '''{% extends 'base.html' %}
{% block title %}Apply for Insurance - SecureBank{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">Apply for Insurance</h1>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p>Insurance application form coming soon...</p>
    </div>
</div>
{% endblock %}''',
}

# Create template files
for filepath, content in templates.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created template: {filepath}")

print("\nAll templates created successfully!")