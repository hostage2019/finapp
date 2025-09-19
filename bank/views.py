from decimal import Decimal, getcontext
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import logging

from accounts.forms import UserLoginForm, TransactionForm, TransferForm, TransactionWithdrawalForm
from accounts.models import CustomUser, Transaction
from .forms import AccountTypeForm, EnquiryForm
from .models import AccType

# Set precision for Decimal operations
getcontext().prec = 2

# Configure logging
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def transferView(request):
    form = TransferForm()
    context = {
        'form': form,
    }
    
    if request.method == 'POST':
        if not request.user.is_superuser:
            alert = 'Your account has been temporarily suspended.'
            messages.error(request, 'Transfer declined.')
            return render(request, 'bank/alert.html', {'alert': alert})
        
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']
            
            try:
                recipient = CustomUser.objects.get(username=recipient_username)
            except CustomUser.DoesNotExist:
                messages.error(request, 'Recipient does not exist.')
                return render(request, 'bank/transfer.html', context)
            
            if request.user.currentBalance >= amount:
                try:
                    # Deduct amount from sender
                    request.user.currentBalance -= Decimal(amount)
                    request.user.save()
                    Transaction.objects.create(
                        user=request.user,
                        amount=-Decimal(amount),
                        activity='Transfer to ' + recipient_username,
                        updatedBy=request.user,
                        date=date
                    )
                    # Add amount to recipient
                    recipient.currentBalance += Decimal(amount)
                    recipient.save()
                    Transaction.objects.create(
                        user=recipient,
                        amount=Decimal(amount),
                        activity='Transfer from ' + request.user.username,
                        updatedBy=request.user,
                        date=date
                    )
                    
                    messages.success(request, 'Transfer successful.')
                    return redirect('transfer')
                except Exception as e:
                    logger.error(f"Error during transfer: {e}")
                    messages.error(request, 'An error occurred during the transfer.')
                    return render(request, 'bank/transfer.html', context)
            else:
                messages.error(request, 'Insufficient balance.')
                return render(request, 'bank/transfer.html', context)
        else:
            messages.error(request, 'Invalid form submission.')
            context['form'] = form
            return render(request, 'bank/transfer.html', context)
    
    return render(request, 'bank/transfer.html', context)


@login_required
def statementView(request, id=None):
    try:
        transactions = Transaction.objects.filter(user_id=id).order_by('-date')
        
        # Pagination
        paginator = Paginator(transactions, 10)  # Show 10 transactions per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'transactions': page_obj,
        }
        return render(request, 'bank/statement.html', context)
    except Transaction.DoesNotExist:
        messages.error(request, 'No transactions found.')
        return render(request, 'bank/statement.html', {})
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        messages.error(request, 'An error occurred while fetching transactions.')
        return render(request, 'bank/statement.html', {})


@login_required
def clientProfileView(request):
    context = {
        'client': request.user,  # Add the current user to the context
    }
    return render(request, 'bank/client_profile.html', context)


@login_required
def depositeView(request, id=None):   
    form = TransactionForm(initial={'user':CustomUser.objects.get(id=id), 'updatedBy':request.user})

    context = {
        'form': form,
    }
    if request.method == "POST":
        user = CustomUser.objects.get(id=id)
        form = TransactionForm(request.POST)
        if form.is_valid():
            trans = form.save(commit=False)
            trans.save()
            user.currentBalance = user.currentBalance + trans.amount
            user.save()
            messages.success(request, 'Account credited successfully')
            form = TransactionForm()
            return render(request, 'bank/deposite.html', context)
        else:
           context['form'] = form
           messages.error(request, 'Account not credited.')
           return render(request, 'bank/deposite.html', context)
        
    return render(request, 'bank/deposite.html', context)

@login_required
def withdrawalView(request, id=None):
    form = TransactionWithdrawalForm(initial={'user': CustomUser.objects.get(id=id), 'updatedBy': request.user})
    context = {
        'form': form,
    }
    if request.method == "POST":
        form = TransactionForm(request.POST)
        user = CustomUser.objects.get(id=id)
        amount = request.POST['amount']
        if form.is_valid():
            trans = form.save(commit=False)
            if user.currentBalance >= Decimal(amount):
                user.currentBalance = Decimal(user.currentBalance) - Decimal(amount)
                trans.save()
                user.save()
                messages.success(request, 'Account debited successfully')
                form = TransactionForm()
                return render(request, 'bank/withdrawal.html', context)
            else:
                messages.error(request, 'Insufficient balance')
                return render(request, 'bank/withdrawal.html', context)
        else:
            context['form'] = form
            messages.error(request, 'Account not debited.')
            print(form.errors)  # Print form errors to debug
            return render(request, 'bank/withdrawal.html', context)
    return render(request, 'bank/withdrawal.html', context)


@login_required
def createAccountTypeView(request):
    form = AccountTypeForm()
    if request.method == 'POST':
        form = AccountTypeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Account type created successfully.')
                return redirect('account_type_list')  # Redirect to the list view to see the new item
            except Exception as e:
                logger.error(f"Error creating account type: {e}")
                messages.error(request, 'An error occurred while creating the account type.')
        else:
            messages.error(request, 'Invalid form submission.')
    return render(request, 'bank/createAccountType.html', {'form': form})


def accountTypeView(request):
    try:
        accountTypes = AccType.objects.all()
        
        # Pagination
        paginator = Paginator(accountTypes, 10)  # Show 10 account types per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'accountTypes': page_obj,
        }
        return render(request, 'bank/accountType.html', context)
    except AccType.DoesNotExist:
        return HttpResponse("No account types found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


def home(request):
    form = UserLoginForm()
    context = {
        'form':form,
    }
    return render(request, 'bank/index.html', context)

def about(request):
    return render(request, 'bank/about.html')


def clientsView(request):
    clients = CustomUser.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'bank/clients.html', context)


@login_required
def clientDashboardView(request):

    transactions = Transaction.objects.filter(user_id=request.user.id).order_by('-date')[:5]
    context = {
        'transactions':transactions,
        'client': request.user,
    }
    return render(request, 'bank/user_dashboard.html', context)


@login_required
def adminDashboardView(request):
    clients = CustomUser.objects.all()
    context = {
        'clients': clients,
    }
    return render(request, 'bank/admin_dashboard.html', context)


def contactView(request):
    form = EnquiryForm()
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message submited')
            return redirect('client_dashboard')
        else:
            messages.error(request, 'Message not submited')
            return render(request, 'bank/contact.html', {'form':form}) 
    else:
        return render(request, 'bank/contact.html', {'form':form})
    
def clientDetailView(request, id=None):
    transactions = Transaction.objects.filter(user_id=id).order_by('-id')[:5]
    clientID = id
    context = {
        'transactions':transactions,
        'client':CustomUser.objects.get(id=id),
        'clientID':clientID,
    }
    return render(request, 'bank/clientDetail.html' , context)

def paymentRequestView(request):
    form = TransferForm()
    if request.method == 'POST':
        amount = request.POST['amount']
        if request.user.currentBalance >= Decimal(amount):
            request.user.currentBalance -= Decimal(amount)
            request.user.save()
            Transaction.objects.create(
                user=request.user,
                amount=-Decimal(amount),
                activity='Payment request',
                updatedBy=request.user,
                date=request.POST['date']
            )
            messages.success(request, 'Payment request successful.')
            return redirect('client_dashboard')
        else:
            messages.error(request, 'Insufficient balance.')
            return redirect('client_dashboard')
    else:
        if not request.user.is_superuser:
            alert = 'Your account has been temporarily suspended. Visit any of our branches for help.'
            messages.error(request, 'Payment request declined.')
            return render(request, 'bank/alert.html', {'alert': alert})
   


def paybillView(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        if request.user.currentBalance >= Decimal(amount):
            request.user.currentBalance -= Decimal(amount)
            request.user.save()
            Transaction.objects.create(
                user=request.user,
                amount=-Decimal(amount),
                activity='Bill payment',
                updatedBy=request.user,
                date=request.POST['date']
            )
            messages.success(request, 'Bill payment successful.')
            return redirect('client_dashboard')
        else:
            messages.error(request, 'Insufficient balance.')
            return redirect('client_dashboard')
    else:
        if not request.user.is_superuser:
            alert = 'Your account has been temporarily suspended. Visit any of our branches for help.'
            messages.error(request, 'Pay bill declined.')
            return render(request, 'bank/alert.html', {'alert': alert})


def loansView(request):
    if not request.user.is_superuser:
            alert = 'Your account has been temporarily suspended. Visit any of our branches for help.'
            messages.error(request, 'Loans declined.')
            return render(request, 'bank/alert.html', {'alert': alert})


def fixedDepositView(request):
    if not request.user.is_superuser:
            alert = 'Your account has been temporarily suspended. Visit any of our branches for help.'
            messages.error(request, 'Fixed deposite declined.')
            return render(request, 'bank/alert.html', {'alert': alert})