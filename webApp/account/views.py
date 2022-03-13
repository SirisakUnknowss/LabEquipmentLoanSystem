from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.http.response import HttpResponse

from .form import AuthenForm
from .models import Account
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def user_login(request):
    if request.method == "GET":
        raise Http404("A Page does not exist")
    form = AuthenForm(request.POST)
    if not form.is_valid():
        return HttpResponse(form.errors, content_type='application/json')
    username = form['username'].value()
    password = form['password'].value()
    print("username --------->" , username)
    print("password --------->" , password)
    
    try:
        account = Account.objects.get(studentID=username, password=password)
        user = account.user
        login(request, user)
        return redirect(reverse('homepage'))
    except ObjectDoesNotExist:
        return redirect(reverse('homepage'))

def user_logout(request):
    logout(request)
    return redirect(reverse('homepage'))