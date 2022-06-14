# Django
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# Module
from django.db.models import Q

#Project
from equipment.models import Equipment
from borrowing.models import EquipmentCart, Order
from account.models import Account

class LabAPIView(GenericAPIView):

    def __init__(self, **kwargs):
        super(LabAPIView, self).__init__()
        self.response = {"error":"", "result":""}

class LabAPIGetView(LabAPIView):

    def __init__(self, **kwargs):
        super(LabAPIGetView, self).__init__()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        self.response["result"] = serializer.data
        return Response(self.response)

class LabListView(LabAPIView):

    def __init__(self, **kwargs):
        super(LabListView, self).__init__()

    def get(self, request, *args, **kwargs):
        queryset                = self.filter_queryset(self.get_queryset())
        serializer              = self.get_serializer(queryset, many=True, context={"request": request})
        self.response["result"] = serializer.data
        return Response(self.response)

class LabListPaginatedView(LabAPIView):

    def __init__(self, **kwargs):
        super(LabListPaginatedView, self).__init__()

    def get(self, request, *args, **kwargs):
        queryset                = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer              = self.get_serializer(queryset, many=True, context={"request": request})
        self.response["result"] = serializer.data
        return Response(self.response)

def checkOverDued(request):
    orders = Order.objects.filter(user=request.user.account, status=Order.STATUS.APPROVED)
    if request.user.account.status == Account.STATUS.ADMIN:
        orders = Order.objects.filter(status=Order.STATUS.APPROVED)
    orders = orders.filter(dateReturn__lt=datetime.now()).update(status=Order.STATUS.OVERDUED)

# Create your views here.
def homepage(request):
    if not(request.user.is_authenticated):
        return render(request, 'base/login.html')
    checkOverDued(request)
    return render(request, 'base/index.html')

def registerpage(request):
    if  request.method == 'POST' and request.POST['accountID']:
        account = Account.objects.get(id=request.POST['accountID'])
        context = { 'account': account }
        return render(request, 'base/signup.html', context)
    return render(request, 'base/signup.html')

def notificationspage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    orders = Order.objects.filter(user=request.user.account, status=Order.STATUS.OVERDUED)
    checkOverDued(request)
    if request.user.account.status == Account.STATUS.ADMIN:
        returned    = Q(status=Order.STATUS.RETURNED)
        waiting     = Q(status=Order.STATUS.WAITING)
        overdued    = Q(status=Order.STATUS.OVERDUED)
        orders      = Order.objects.filter(waiting | returned | overdued)
    context         = { 'orders': orders }
    return render(request, 'pages/notifications_page.html', context)

def informationpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    waiting     = Q(status=Order.STATUS.WAITING)
    approved    = Q(status=Order.STATUS.APPROVED)
    overdued    = Q(status=Order.STATUS.OVERDUED)
    returned    = Q(status=Order.STATUS.RETURNED)
    canceled    = Q(status=Order.STATUS.CANCELED)
    completed   = Q(status=Order.STATUS.COMPLETED)
    disapproved = Q(status=Order.STATUS.DISAPPROVED)
    orders      = Order.objects.filter(waiting | approved | returned)
    if request.user.account.status == Account.STATUS.USER:
        orders  = orders.filter(user=request.user.account)
    context     = { 'orders': orders }
    return render(request, 'pages/information_page.html', context)

def borrowinghistorypage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    waiting     = Q(status=Order.STATUS.WAITING)
    approved    = Q(status=Order.STATUS.APPROVED)
    overdued    = Q(status=Order.STATUS.OVERDUED)
    returned    = Q(status=Order.STATUS.RETURNED)
    canceled    = Q(status=Order.STATUS.CANCELED)
    completed   = Q(status=Order.STATUS.COMPLETED)
    disapproved = Q(status=Order.STATUS.DISAPPROVED)
    orders      = Order.objects.filter(disapproved | canceled | completed)
    if request.user.account.status == Account.STATUS.USER:
        orders  = orders.filter(user=request.user.account)
    context     = { 'orders': orders }
    return render(request, 'pages/borrowing_history_page.html', context)

def analysispage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    context = { 'orders': orderAll(), 'accounts': accountAll() }
    return render(request, 'pages/analysis_page.html', context)
    
def accountAll():
    admin               = Q(status=Account.STATUS.ADMIN)
    user                = Q(status=Account.STATUS.USER)
    account             = dict()
    accounts            = Account.objects.all()
    account['all']      = accounts.count()
    account['user']     = accounts.filter(user).count()
    account['admin']    = accounts.filter(admin).count()
    return account

def orderAll():
    waiting     = Q(status=Order.STATUS.WAITING)
    approved    = Q(status=Order.STATUS.APPROVED)
    overdued    = Q(status=Order.STATUS.OVERDUED)
    returned    = Q(status=Order.STATUS.RETURNED)
    canceled    = Q(status=Order.STATUS.CANCELED)
    completed   = Q(status=Order.STATUS.COMPLETED)
    disapproved = Q(status=Order.STATUS.DISAPPROVED)
    order       = dict()
    orders      = Order.objects.all()

    order['all']            = orders.count()
    order['waiting']        = orders.filter(waiting).count()
    order['canceled']       = orders.filter(canceled).count()
    order['returned']       = orders.filter(returned).count()
    order['approved']       = orders.filter(approved).count()
    order['overdued']       = orders.filter(overdued).count()
    order['completed']      = orders.filter(completed).count()
    order['disapproved']    = orders.filter(disapproved).count()
    return order


def contactpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    return render(request, 'pages/contact_page.html')

def profilepage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    return render(request, 'pages/user_profile.html')

def addequipmentpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    if request.method == 'POST':
        equipmentID = request.POST['EquipmentID']
        equipment = Equipment.objects.filter(id=equipmentID)
        if equipment.exists():
            context = { 'equipment': equipment.first() }
            return render(request, 'pages/add_equipment.html', context)
        else:
            return redirect(reverse('equipment-list'))

    return render(request, 'pages/add_equipment.html')

def equipmentlistpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    equipments = Equipment.objects.all().values()
    context = { 'equipments': equipments }
    return render(request, 'pages/equipment_list_page.html', context)

def equipmentdetailpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    if request.method == 'GET':
        return redirect(reverse('homepage'))
    status      = request.POST['StatusBorrowing']
    equipmentID = request.POST['EquipmentID']
    try:
        order   = Order.objects.get(id=equipmentID, status=status)
        context = { 'order': order, 'status': status }
        return render(request, 'pages/equipment_detail_page.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('equipment-list'))

def equipmentcartlistpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    equipmentsCart = EquipmentCart.objects.filter(user=request.user.account)
    context = { 'equipmentsCart': equipmentsCart }
    return render(request, 'pages/cart_equipment_page.html', context)

def usermanagementpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    return render(request, 'pages/user_management_page.html')

def usereditpage(request):
    if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
        return redirect(reverse('homepage'))
    context = dict()
    if request.method == 'POST':
        status      = request.POST['status']
        username    = request.POST['username']
        account     = Account.objects.filter(studentID=username)
        context['account'] = 'notfound'
        context['status'] = ''
        if account.exists():
            context['account'] = account[0]
            context['status'] = 'view'
            if status == 'edit':
                context['status'] = 'edit'
    return render(request, 'pages/manage_user_page.html', context)
    