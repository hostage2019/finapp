from django import forms
from django.forms import ModelForm

from .models import AccType, Enquiry


class AccountTypeForm(ModelForm):
    accTypeName = forms.CharField(label='Account Type',widget= forms.TextInput(attrs={'class': 'form-control'}))
    #password = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = AccType
        fields = ['accTypeName']


class EnquiryForm(ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control mb-1','placeholder':'Title'}))
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'class':'form-control mb-3','placeholder':'Message'}))
    sender = forms.CharField(label='', widget=forms.EmailInput(attrs={'class':'form-control mb-1','placeholder':'Email'}))

    class Meta:
        model = Enquiry
        fields = ['title', 'sender', 'message']