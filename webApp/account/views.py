from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.contrib.auth.models import User
from django.http.response import HttpResponse

from .form import AuthenForm, RegisterForm
from .models import Account
from .serializers import SlzAccountCreate
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

def user_register(request):
    if request.method == "GET":
        raise Http404("A Page does not exist")
    form = RegisterForm(request.POST)
    if not form.is_valid():
        return HttpResponse(form.errors, content_type='application/json')
    username = form['username'].value()
    password = form['password'].value()
    
    try:
        account = Account.objects.get(studentID=username)
        return redirect(reverse('registerpage'))
    except ObjectDoesNotExist:
        user = User.objects.create_user(username=username, email=None, password=password, is_active=True)
        account = createAccount(user=user, studentID=username, password=password)
        account.save()
        user = account.user
        login(request, user)
        return redirect(reverse('homepage'))
    
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