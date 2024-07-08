from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.forms import UserLoginForm, AdminUserRegisterForm

# Create your views here.
def signInView(request):
    form = UserLoginForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have login in successfully.')
            if user.is_superuser:
                return redirect('admin_dashboard')
            else: 
                return redirect('client_dashboard')
        else:
            form = UserLoginForm(request.POST)
            context['form'] = form
            messages.error(request, 'Account Number or password is incorrect')
            return render(request, 'accounts/signIn.html', context)
    else:
        return render(request, 'accounts/signIn.html', context)
    

def adminRegisterView(request):
    form = AdminUserRegisterForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = AdminUserRegisterForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.set_password(request.POST['password'])
            client.save()
            messages.success(request,  'Client registered Successfully.')
            return redirect('clients')
        else:
            context['form'] = form
            messages.error(request, 'Client not registered.')
            return render(request, 'accounts/admin_register.html', context)
    else:  
        return render(request, 'accounts/admin_register.html', context)
    

def signOutView(request):
    logout(request)
    return redirect('home')