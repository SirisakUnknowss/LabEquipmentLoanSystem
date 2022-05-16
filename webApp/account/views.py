from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .form import AuthenForm, RegisterForm
from .models import Account
from .serializers import SlzAccountCreate

# Create your views here.

def user_login(request):
    if request.method == "GET":
        raise Http404("A Page does not exist")
    form = AuthenForm(request.POST)
    if not form.is_valid():
        return HttpResponse(form.errors, content_type='application/json')
    try:
        account = Account.objects.get(studentID=form['username'].data, password=form['password'].data)
        user = account.user
        login(request, user)
        return redirect(reverse('homepage'))
    except ObjectDoesNotExist:
        return redirect(reverse('homepage'))

def user_logout(request):
    logout(request)
    return redirect(reverse('homepage'))

def user_register(request):
    if request.method == "GET":
        raise Http404("A Page does not exist")
    form = RegisterForm(request.POST)
    if not form.is_valid():
        return HttpResponse(form.errors, content_type='application/json')
    check_account_exist(form)
    check_password(form)
    user    = create_user_data(form)
    account = createAccount(user, form)
    user    = account.user
    login(request, user)
    return redirect(reverse('homepage'))

def create_user_data(form:RegisterForm):
    user = User.objects.create_user(
        username=form['username'].data, 
        email=form['email'].data, 
        password=form['password'].data, 
        is_active=True
        )
    return user

def check_account_exist(form:RegisterForm):
    account = Account.objects.filter(studentID=form['username'].value)
    if account.exists():
        return Http404("Already have this account.")

def check_password(form:RegisterForm):
    if form['password'].value != form['repassword'].value:
        return Http404("Password and confirm password does not match.")
    
def createAccount(user:User, form:RegisterForm):
    branch = split_branch(form['branch'].data)
    data = {
        "user": user.id,
        "studentID": form['username'].data,
        "password": form['password'].data,
        "nameprefix": form['nameprefix'].data,
        "firstname": form['firstname'].data,
        "lastname": form['lastname'].data,
        "email": form['email'].data,
        "phone": form['phone'].data,
        "levelclass": form['levelclass'].data,
        "branch": branch['branch'],
        "faculty": branch['faculty'],
        "status": 'user'
    }
    serializer = SlzAccountCreate(data=data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    account = Account(
        user=user,
        studentID=data['studentID'],
        password=data['password'],
        nameprefix=data['nameprefix'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        phone=data['phone'],
        levelclass=data['levelclass'],
        branch=data['branch'],
        faculty=data['faculty'],
        status=data['status'],
        )
    account.save()
    return account

def split_branch(value:str):
    strSplit = value.split('_')
    data = { 'branch': strSplit[1], 'faculty': strSplit[0] }
    return data