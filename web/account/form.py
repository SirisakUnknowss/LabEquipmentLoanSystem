from django.shortcuts import redirect
from django.urls import reverse
# Django
from django import forms
#Project
from .models import Account

class AuthenForm(forms.Form):
    username = forms.CharField(max_length=10)
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
    category    = forms.ChoiceField(choices=Account.CATEGORY.choices)
    branch      = forms.CharField(max_length=50)

class UpdateForm(forms.Form):
    nameprefix  = forms.CharField(max_length=10)
    firstname   = forms.CharField(max_length=50)
    lastname    = forms.CharField(max_length=50)
    email       = forms.EmailField(max_length=50)
    phone       = forms.CharField(max_length=10)
    levelclass  = forms.ChoiceField(choices=Account.LEVEL_CLASS.choices)
    category    = forms.ChoiceField(choices=Account.CATEGORY.choices)
    branch      = forms.CharField(max_length=50)