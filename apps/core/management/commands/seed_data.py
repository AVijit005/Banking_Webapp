# apps/core/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import BankAccount, Branch
from apps.transactions.models import Transaction
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with demo data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create branch
        branch = Branch.objects.create(
            branch_id='BR001',
            name='Main Branch',
            address='123 Financial Street',
            city='New York',
            state='NY',
            postal_code='10001',
            phone_number='+1234567890',
            email='main@securebank.com'
        )
        
        # Create Admin
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@securebank.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        # Create Manager
        manager = User.objects.create_user(
            username='manager',
            email='manager@securebank.com',
            password='manager123',
            first_name='John',
            last_name='Manager',
            role='manager'
        )
        
        # Create Employee
        employee = User.objects.create_user(
            username='employee',
            email='employee@securebank.com',
            password='employee123',
            first_name='Jane',
            last_name='Employee',
            role='employee'
        )
        
        # Create Customers
        customer1 = User.objects.create_user(
            username='customer1',
            email='customer1@example.com',
            password='customer123',
            first_name='Alice',
            last_name='Johnson',
            role='customer',
            phone_number='+1987654321'
        )
        
        customer2 = User.objects.create_user(
            username='customer2',
            email='customer2@example.com',
            password='customer123',
            first_name='Bob',
            last_name='Smith',
            role='customer',
            phone_number='+1876543210'
        )
        
        # Create Bank Accounts
        account1 = BankAccount.objects.create(
            account_number='100000000001',
            user=customer1,
            account_type='savings',
            branch=branch,
            balance=5000.00,
            minimum_balance=500.00,
            interest_rate=2.5
        )
        
        account2 = BankAccount.objects.create(
            account_number='100000000002',
            user=customer1,
            account_type='current',
            branch=branch,
            balance=10000.00,
            minimum_balance=1000.00
        )
        
        account3 = BankAccount.objects.create(
            account_number='200000000001',
            user=customer2,
            account_type='savings',
            branch=branch,
            balance=7500.00,
            minimum_balance=500.00,
            interest_rate=2.5
        )
        
        # Create sample transactions
        for i in range(20):
            Transaction.objects.create(
                from_account=random.choice([account1, account2, account3]),
                to_account=random.choice([account1, account2, account3]),
                transaction_type=random.choice(['transfer', 'deposit', 'withdrawal']),
                amount=random.uniform(10, 500),
                status='completed',
                reference_number=f'TXN{i:06d}',
                initiated_by=random.choice([customer1, customer2]),
                timestamp=datetime.now() - timedelta(days=random.randint(1, 30))
            )
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('Login credentials:')
        self.stdout.write('Admin: username=admin, password=admin123')
        self.stdout.write('Manager: username=manager, password=manager123')
        self.stdout.write('Employee: username=employee, password=employee123')
        self.stdout.write('Customer 1: username=customer1, password=customer123')
        self.stdout.write('Customer 2: username=customer2, password=customer123')