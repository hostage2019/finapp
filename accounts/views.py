from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.forms import UserLoginForm, AdminUserRegisterForm, AdminUserEditForm
from .models import CustomUser

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
        form = AdminUserRegisterForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            client = form.save(commit=False)
            client.set_password(form.cleaned_data['password'])  # Use cleaned_data to get the password
            client.save()
            messages.success(request,  'Client registered Successfully.')
            return redirect('clients')
        else:
            context['form'] = form
            messages.error(request, 'Client not registered.')
            print(form.errors)  # Print form errors to debug
            return render(request, 'accounts/admin_register.html', context)
    else:  
        return render(request, 'accounts/admin_register.html', context)
    

def signOutView(request):
    logout(request)
    return redirect('home')

def editClientView(request, id=None):

    form = AdminUserEditForm(instance=CustomUser.objects.get(id=id))
    context = {
        'form':form,
        'edit':True,
    }
    if request.method == "POST":
        form = AdminUserEditForm(request.POST, request.FILES, instance=CustomUser.objects.get(id=id))
        if form.is_valid():
            form.save()
            messages.success(request, 'Client update succesfull')
            return redirect('clients')
        else:
            return render(request, 'accounts/admin_register.html', context)  
    else:
        return render(request, 'accounts/admin_register.html', context)