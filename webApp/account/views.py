from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.http import Http404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from rest_framework.exceptions import ValidationError

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
        account = Account.objects.get(studentID=form['username'].value, password=form['password'].value)
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
        return HttpResponse(form, content_type='application/json')
    check_account_exist(form)
    user = User.objects.create_user(username=form.username, email=form.email, password=form.password, is_active=True)
    account = createAccount(user=form.user, studentID=form.username, password=form.password)
    account.save()
    user = account.user
    login(request, user)
    return redirect(reverse('homepage'))

def check_account_exist(form:RegisterForm):
    account = Account.objects.filter(studentID=form.username)
    if account.exists():
        return Http404("Already have this account.")
    if form.password != form.repassword:
        return Http404("Password and confirm password does not match.")
    
def createAccount(user, studentID, password, email, firstname, lastname, gender, phone, levelclass, branch, faculty, status):
    data = {
        "user": user.id,
        "studentID": studentID,
        "password": password,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "phone": phone,
        "gender": gender,
        "levelclass": levelclass,
        "branch": branch,
        "faculty": faculty,
        "status": status
    }
    serializer = SlzAccountCreate(data=data)
    serializer.is_valid(raise_exception=True)
    customer = Account(
        user=user,
        studentID=studentID,
        password=password,
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        gender=gender,
        levelclass=levelclass,
        branch=branch,
        faculty=faculty,
        status=status,
        )
    customer.save()
    return customer