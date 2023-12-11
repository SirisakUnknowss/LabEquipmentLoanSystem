# Django
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Project
from base.functions import uploadImage
from account.form import AuthenForm, RegisterForm, UpdateForm
from account.models import Account, getClassPath
from account.serializers import SlzAccountCreate

# Create your views here.

def user_login(request):
    if request.method == "GET":
        raise Http404("A Page does not exist")
    form = AuthenForm(request.POST)
    if not form.is_valid():
        return redirect(reverse('homepage'))
    try:
        username = form['username'].data
        password = form['password'].data
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
        context = { 'form': form.errors }
        return render(request, 'base/signup.html', context)
    account = Account.objects.filter(studentID=form['username'].data)
    if account.exists():
        context = { 'accountExists': 'บัญชีผู้ใช้งานนี้มีอยู่แล้ว' }
        return render(request, 'base/signup.html', context)
    user = User.objects.filter(username=form['username'].data)
    user.delete()
    if form['password'].data != form['repassword'].data:
        context = { 'password': 'รหัสผ่านไม่ตรงกัน' }
        return render(request, 'base/signup.html', context)
    user    = create_user_data(form)
    account = createAccount(request, user, form)
    user    = account.user
    if request.user.is_authenticated:
        account = request.user.account
        if account.status == "admin":
            return redirect(reverse('userManagementPage'))
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
    
def createAccount(request, user:User, form:RegisterForm):
    branch = split_branch(form['branch'].data)
    branchs = request.POST['branch']
    category = request.POST['category']
    if branchs == 'Other_Other':
        branch['branch'] = request.POST['branchOther']
    categoryOther = request.POST['categoryOther']
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
        "category": category,
        "categoryOther": categoryOther,
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
        category=data['category'],
        categoryOther=data['categoryOther'],
        status=data['status'],
        )
    account.save()
    if not(request.FILES.get('upload', False)):
        return account
    upload  = request.FILES['upload']
    name    = getClassPath(account, data['studentID'])
    uploadImage(name, upload, account)
    return account

def split_branch(value:str):
    strSplit = value.split('_')
    data = { 'branch': strSplit[1], 'faculty': strSplit[0] }
    return data

def user_edit(request):
    if request.method == "GET":
        raise Http404("A Page does not exist")
    if str(request.user.account.id) != str(request.POST['accountID']):
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
    if request.POST['accountID']:
        data = setData(request)
        editProfile(data)
    if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
        return redirect(reverse('profilePage'))
    return redirect(reverse('userEditPage'))

def setData(request):
    form = UpdateForm(request.POST)
    if not form.is_valid():
        return HttpResponse(form.errors, content_type='application/json')
    user        = Account.objects.get(id=request.POST['accountID'])
    branch      = split_branch(form['branch'].data)
    branchs     = request.POST['branch']
    category    = request.POST['category']
    if branchs == 'Other_Other':
        branch['branch'] = request.POST['branchOther']
    if category == 'other':
        category = request.POST['categoryOther']
    data = {
        "studentID": user.studentID,
        "id": request.POST['accountID'],
        "user": user.id,
        "nameprefix": form['nameprefix'].data,
        "firstname": form['firstname'].data,
        "lastname": form['lastname'].data,
        "email": form['email'].data,
        "phone": form['phone'].data,
        "levelclass": form['levelclass'].data,
        "branch": branch['branch'],
        "faculty": branch['faculty'],
        "category": category,
        "status": 'user',
        "image": None,
    }
    if request.FILES.get('upload', False):
        data['image'] = request.FILES['upload']
    return data

def editProfile(data):
    Account.objects.filter(id=data['id']).update(
        nameprefix=data['nameprefix'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        phone=data['phone'],
        levelclass=data['levelclass'],
        branch=data['branch'],
        faculty=data['faculty'],
        category=data['category'],
        status=data['status'],
        )
    if data['image'] == None:
        return
    account = Account.objects.get(id=data['id'])
    name    = getClassPath(account, data['studentID'])
    uploadImage(name, data['image'], account)

def delete_account(request):
    if request.method == "GET":
        raise Http404("A Page does not exist")
    if request.user.account.status != Account.STATUS.ADMIN:
        return redirect(reverse('homepage'))
    if request.POST['accountID']:
        Account.objects.filter(id=request.POST['accountID']).delete()
    return redirect(reverse('userEditPage'))