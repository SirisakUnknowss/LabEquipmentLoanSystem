# Django
from django import forms

class AuthenForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)