from django.shortcuts import redirect
from django.urls import reverse
# Django
from django import forms
from django.contrib.auth.models import User
#Project
from .models import Account

class AuthenForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        try:
            username = cleaned_data['username']
            password = cleaned_data['password']
            if not username and not password:
                self.add_error('username', "UserName incorrect!")
                self.add_error('password', "Password incorrect!")
            return cleaned_data
        except:
            return redirect(reverse('homepage'))

class RegisterForm(forms.Form):
    username    = forms.CharField(max_length=50)
    password    = forms.CharField(max_length=50)
    repassword  = forms.CharField(max_length=50)
    nameprefix  = forms.CharField(max_length=10)
    firstname   = forms.CharField(max_length=50)
    lastname    = forms.CharField(max_length=50)
    email       = forms.EmailField(max_length=50)
    phone       = forms.CharField(max_length=10)
    levelclass  = forms.ChoiceField(choices=Account.LEVEL_CLASS.choices)
    branch      = forms.CharField(max_length=50)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        except User.DoesNotExist:
            return username

class UpdateForm(forms.Form):
    nameprefix  = forms.CharField(max_length=10)
    firstname   = forms.CharField(max_length=50)
    lastname    = forms.CharField(max_length=50)
    email       = forms.EmailField(max_length=50)
    phone       = forms.CharField(max_length=10)
    levelclass  = forms.ChoiceField(choices=Account.LEVEL_CLASS.choices)
    branch      = forms.CharField(max_length=50)