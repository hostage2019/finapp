from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from .models import CustomUser, Transaction
from bank.models import AccType


class TransferForm(forms.Form):
    recipient = forms.CharField( label='Recipient', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'12345'}))
    amount = forms.DecimalField(decimal_places=2, widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0.00'}))
    date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))




class TransactionForm(ModelForm):
    amount = forms.CharField(label='Amount',widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0.00'}))
    activity = forms.CharField(label='',initial='deposit',widget= forms.HiddenInput())
    updatedBy = forms.ModelChoiceField(label='', queryset=CustomUser.objects.all(),widget= forms.HiddenInput())
    user = forms.ModelChoiceField(label='', queryset=CustomUser.objects.all(), widget= forms.HiddenInput())
    date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))

    
    class Meta:
        model = Transaction
        fields = ['activity', 'amount', 'updatedBy', 'user', 'date']

class TransactionWithdrawalForm(ModelForm):
    amount = forms.CharField(label='Amount',widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0.00'}))
    activity = forms.CharField(label='',initial='withdrawal',widget= forms.HiddenInput())
    updatedBy = forms.ModelChoiceField(label='', queryset=CustomUser.objects.all(),widget= forms.HiddenInput())
    user = forms.ModelChoiceField(label='', queryset=CustomUser.objects.all(), widget= forms.HiddenInput())
    date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))

    
    class Meta:
        model = Transaction
        fields = ['activity', 'amount', 'updatedBy', 'user', 'date']


class UserLoginForm(ModelForm):
    username = forms.CharField(label='Account Number',widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']



class AdminUserRegisterForm(ModelForm):
    image = forms.ImageField(label='Account holder image',widget= forms.FileInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Account Number',widget= forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name',widget= forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label='Middle Name',widget= forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name',widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirm',widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email',widget= forms.EmailInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(label='Date Of Birth',widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    accType = forms.ModelChoiceField(label='Type Of Account', queryset=AccType.objects.all(), initial={},widget= forms.Select(attrs={'class': 'form-control'}))



    class Meta:
        model = CustomUser
        fields = ['image','username', 'first_name', 'middle_name', 'last_name', 'birth_date', 'email','accType', 'password']


class AdminUserEditForm(ModelForm):
    image = forms.ImageField(label='Account holder image',widget= forms.FileInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Account Number',widget= forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name',widget= forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label='Middle Name',widget= forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name',widget= forms.TextInput(attrs={'class': 'form-control'}))
    #password = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    #password2 = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email',widget= forms.EmailInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(label='Date Of Birth',widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    accType = forms.ModelChoiceField(label='Type Of Account', queryset=AccType.objects.all(), initial={},widget= forms.Select(attrs={'class': 'form-control'}))



    class Meta:
        model = CustomUser
        fields = ['image','username', 'first_name', 'middle_name', 'last_name', 'birth_date', 'email','accType']
