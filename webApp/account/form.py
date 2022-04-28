# Django
from django import forms
#Project
from .models import Account

class AuthenForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        if not username and not password:
            self.add_error('username', "UserName incorrect!")
            self.add_error('password', "Password incorrect!")

class RegisterForm(forms.Form):
    username    = forms.CharField(max_length=50)
    password    = forms.CharField(max_length=50)
    repassword  = forms.CharField(max_length=50)
    firstname   = forms.CharField(max_length=50)
    email       = forms.EmailField(max_length=50)
    phone       = forms.CharField(max_length=10)
    levelclass  = forms.ChoiceField(choices=Account.LEVEL_CLASS.choices)
    branch      = forms.CharField(max_length=50)
    # faculty     = forms.CharField(max_length=50)
    # status      = forms.ChoiceField(choices=Account.STATUS.choices)