# apps/transactions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Transaction, QRPayment
from apps.accounts.models import BankAccount
from apps.core.forms import MoneyTransferForm
import qrcode
import io
from django.core.files.base import ContentFile
import uuid

@login_required
def transaction_list(request):
    """List all transactions for the user"""
    transactions = Transaction.objects.filter(
        from_account__user=request.user
    ).order_by('-timestamp')
    
    # Pagination
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'transactions': page_obj,
        'total_transactions': transactions.count(),
    }
    return render(request, 'transactions/transaction_list.html', context)

@login_required
def transaction_detail(request, transaction_id):
    """Detail view for a specific transaction"""
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id, from_account__user=request.user)
    
    context = {
        'transaction': transaction,
    }
    return render(request, 'transactions/transaction_detail.html', context)

@login_required
def money_transfer(request):
    """Money transfer form and processing"""
    if request.method == 'POST':
        form = MoneyTransferForm(request.user, request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    from_account = form.cleaned_data['from_account']
                    to_account_number = form.cleaned_data['to_account_number']
                    amount = form.cleaned_data['amount']
                    transfer_type = form.cleaned_data['transfer_type']
                    description = form.cleaned_data.get('description', '')
                    
                    # Check if account has sufficient balance
                    if from_account.balance < amount:
                        messages.error(request, 'Insufficient balance for this transaction.')
                        return render(request, 'transactions/money_transfer.html', {'form': form})
                    
                    # Find destination account
                    try:
                        to_account = BankAccount.objects.get(account_number=to_account_number)
                    except BankAccount.DoesNotExist:
                        messages.error(request, 'Destination account not found.')
                        return render(request, 'transactions/money_transfer.html', {'form': form})
                    
                    # Create transaction record
                    new_transaction = Transaction.objects.create(
                        from_account=from_account,
                        to_account=to_account,
                        transaction_type='transfer',
                        amount=amount,
                        status='completed',
                        payment_method='online',
                        reference_number=f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}",
                        description=description,
                        initiated_by=request.user,
                        completed_at=timezone.now()
                    )
                    
                    # Update account balances
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    
                    messages.success(request, f'Transfer of ${amount} completed successfully!')
                    return redirect('transaction_detail', transaction_id=new_transaction.transaction_id)
                    
            except Exception as e:
                messages.error(request, f'Transaction failed: {str(e)}')
    else:
        form = MoneyTransferForm(request.user)
    
    return render(request, 'transactions/money_transfer.html', {'form': form})

@login_required
def qr_generate(request):
    """Generate QR code for payment"""
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        amount = request.POST.get('amount')
        purpose = request.POST.get('purpose', 'Payment')
        
        try:
            account = BankAccount.objects.get(account_number=account_number, user=request.user)
            
            # Generate QR code
            qr_data = {
                'account_number': account_number,
                'amount': amount,
                'purpose': purpose,
                'timestamp': timezone.now().isoformat()
            }
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(str(qr_data))
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code
            buffer = io.BytesIO()
            qr_image.save(buffer, format='PNG')
            qr_file = ContentFile(buffer.getvalue())
            
            qr_payment = QRPayment.objects.create(
                account=account,
                amount=amount if amount else None,
                purpose=purpose,
                qr_code_image=qr_file
            )
            
            messages.success(request, 'QR code generated successfully!')
            return redirect('qr_payment', qr_id=qr_payment.qr_code_id)
            
        except BankAccount.DoesNotExist:
            messages.error(request, 'Account not found.')
        except Exception as e:
            messages.error(request, f'Error generating QR code: {str(e)}')
    
    # Get user's accounts
    accounts = BankAccount.objects.filter(user=request.user, status='active')
    
    context = {
        'accounts': accounts,
    }
    return render(request, 'transactions/qr_generate.html', context)

@login_required
def qr_payment(request, qr_id):
    """Display QR code for payment"""
    qr_payment = get_object_or_404(QRPayment, qr_code_id=qr_id, account__user=request.user)
    
    context = {
        'qr_payment': qr_payment,
    }
    return render(request, 'transactions/qr_payment.html', context)

@login_required
def qr_scan(request):
    """QR code scanning interface"""
    return render(request, 'transactions/qr_scan.html')

@login_required
def process_qr_payment(request):
    """Process QR code payment with enhanced security"""
    if request.method == 'POST':
        try:
            # Validate request headers for API authentication
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Unauthorized - Missing authentication token'}, status=401)

            # Parse JSON data
            data = request.json()
            qr_data = data.get('qr_data')

            if not qr_data:
                return JsonResponse({'error': 'Invalid QR data'}, status=400)

            # Parse QR data
            account_number = qr_data.get('account_number')
            amount = qr_data.get('amount')
            purpose = qr_data.get('purpose', 'QR Payment')

            # Validate required fields
            if not account_number or not amount:
                return JsonResponse({'error': 'Missing required fields: account_number, amount'}, status=400)

            # Validate amount is positive
            try:
                amount = float(amount)
                if amount <= 0:
                    return JsonResponse({'error': 'Amount must be positive'}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid amount format'}, status=400)

            # Find source account (current user's account)
            from_account = BankAccount.objects.filter(user=request.user, status='active').first()
            if not from_account:
                return JsonResponse({'error': 'No active account found'}, status=400)

            # Find destination account
            try:
                to_account = BankAccount.objects.get(account_number=account_number)
            except BankAccount.DoesNotExist:
                return JsonResponse({'error': 'Destination account not found'}, status=400)

            # Check balance
            if from_account.balance < amount:
                return JsonResponse({'error': 'Insufficient balance'}, status=400)

            # Additional security: Check for suspicious activity
            if amount > from_account.daily_withdrawal_limit:
                return JsonResponse({'error': 'Amount exceeds daily withdrawal limit'}, status=400)

            # Create transaction
            with transaction.atomic():
                new_transaction = Transaction.objects.create(
                    from_account=from_account,
                    to_account=to_account,
                    transaction_type='payment',
                    amount=amount,
                    status='completed',
                    payment_method='qr',
                    reference_number=f"QR{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    description=purpose,
                    initiated_by=request.user,
                    completed_at=timezone.now()
                )

                # Update balances
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()

            return JsonResponse({
                'success': True,
                'transaction_id': str(new_transaction.transaction_id),
                'message': 'Payment processed successfully'
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
