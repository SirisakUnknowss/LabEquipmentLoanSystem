# Python
import json, os, time, csv
from datetime import datetime
# Django
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# Module
from django.db.models import Q

#Project
from account.models import Account
from account.admin import AccountResource
from base.models import DataWeb
from borrowing.admin import OrderModelAdmin, OrderModelResource
from borrowing.models import EquipmentCart, Order
from equipment.models import Equipment
from scientificInstrument.models import ScientificInstrument, Booking
from settings.base import MEDIA_ROOT

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
    returned    = Q(status=Order.STATUS.RETURNED)
    orders      = Order.objects.filter(waiting | approved | returned)
    if request.user.account.status == Account.STATUS.USER:
        orders  = orders.filter(user=request.user.account)
    context     = { 'orders': orders }
    return render(request, 'pages/information_page.html', context)

def borrowinghistorypage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
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
    context = { 'orders': orderAll(), 'accounts': accountAll(), 'equipments': topEquipment() }
    return render(request, 'pages/analysis_page.html', context)

def topEquipment():
    equipments = Equipment.objects.all().order_by('-statistics').filter(statistics__gt=1)
    return equipments
    
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
    dataWeb = DataWeb.objects.all().first()
    context = { 'dataWeb': dataWeb }
    return render(request, 'pages/contact_page.html', context)

def profilepage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    approved    = Q(status=Order.STATUS.APPROVED)
    overdued    = Q(status=Order.STATUS.OVERDUED)
    returned    = Q(status=Order.STATUS.RETURNED)
    
    context     = { }
    if request.user.account.status == Account.STATUS.USER:
        orders  = Order.objects.filter(approved | returned | overdued)
        orders  = orders.filter(user=request.user.account)
        context = { 'orders': orders }
    return render(request, 'pages/user_profile.html', context)

def addequipmentpage(request):
    if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
        return redirect(reverse('homepage'))
    if request.method == 'POST':
        equipmentID = request.POST['EquipmentID']
        equipment = Equipment.objects.filter(id=equipmentID)
        if equipment.exists():
            context = { 'equipment': equipment.first() }
            return render(request, 'pages/add_equipment.html', context)
        return redirect(reverse('equipment-list'))
    return render(request, 'pages/add_equipment.html')

def equipmentlistpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    equipments = Equipment.objects.all().order_by('name')
    if request.method == 'POST':
        nameequipment   = request.POST['nameequipment']
        name            = Q(name__contains=nameequipment)
        equipments      = Equipment.objects.filter(name).order_by('name')
    equipmentsJson = serializers.serialize("json", equipments)
    context = { 'equipments': equipments, 'equipmentsJson': equipmentsJson }
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
    context['accounts'] = Account.objects.all().order_by('id')
    if request.method == 'POST':
        status      = request.POST['status']
        username    = request.POST['username']
        studentID   = Q(studentID__contains=username)
        firstname   = Q(firstname__contains=username)
        lastname    = Q(lastname__contains=username)
        branch      = Q(branch__contains=username)
        accounts    = Account.objects.filter(studentID | firstname | lastname | branch).order_by('id')
        context['accounts'] = 'notfound'
        context['status'] = ''
        if accounts.exists():
            context['accounts'] = accounts
            context['status'] = 'view'
            if status == 'edit':
                context['status'] = 'edit'
    return render(request, 'pages/manage_user_page.html', context)

class ExportUserData(LabAPIView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        filePath = self.writeFile()
        # self.response['result'] = filePath
        return self.download_file(filePath)
    
    def download_file(self, file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = 'attachment; filename="userdata.csv"'
        response['Content-Type'] = 'application/octet-stream'
        return response

    def writeFile(self):
        userFileDir = "UserData"
        dirPath = "{}/{}".format(MEDIA_ROOT, userFileDir)
        if not(os.path.exists(dirPath)):
            os.makedirs(dirPath)
        # datestr = str(time.strftime("%Y%m%d_%H%M%S"))
        fileName = "userdata.csv"
        filePath = "{}/{}".format(dirPath, fileName)
        dataset = AccountResource().export()
        with open(filePath, "w") as f:
            f.write(dataset.csv)
        return "{}/{}/{}".format(MEDIA_ROOT, userFileDir, fileName)

class ExportBorrowingData(LabAPIView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        # self.response['result'] = filePath
        return self.download_file(filePath, fileName)
    
    def download_file(self, file_path, fileName):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{fileName}"'
        response['Content-Type'] = 'application/octet-stream'
        return response

    def writeFile(self, parameter_value):
        userFileDir = "OrderData"
        dirPath = "{}/{}".format(MEDIA_ROOT, userFileDir)
        if not(os.path.exists(dirPath)):
            os.makedirs(dirPath)
        # datestr = str(time.strftime("%Y%m%d_%H%M%S"))
        queryset = Order.objects.filter(status=parameter_value)
        fileName = f"{parameter_value}Data.csv"
        if parameter_value == '':
            queryset = Order.objects.all()
            fileName = "allData.csv"
        filePath = "{}/{}".format(dirPath, fileName)
        dataset = OrderModelResource().export(queryset=queryset)
        with open(filePath, "w") as f:
            f.write(dataset.csv)
        return "{}/{}/{}".format(MEDIA_ROOT, userFileDir, fileName), fileName

class ExportEquipments(LabAPIView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        return self.download_file(filePath, fileName)
    
    def download_file(self, file_path, fileName):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{fileName}"'
        response['Content-Type'] = 'application/octet-stream'
        return response

    def writeFile(self, parameter_value):
        userFileDir = "OrderData"
        dirPath = "{}/{}".format(MEDIA_ROOT, userFileDir)
        if not(os.path.exists(dirPath)):
            os.makedirs(dirPath)
        queryset = Equipment.objects.all()
        if parameter_value != "":
            queryset = Equipment.objects.all().order_by('-statistics').filter(statistics__gt=1)
        fileName = f"Equipments{parameter_value}Data.csv"
        filePath = "{}/{}".format(dirPath, fileName)
        dataset = OrderModelResource().export(queryset=queryset)
        with open(filePath, "w") as f:
            f.write(dataset.csv)
        return "{}/{}/{}".format(MEDIA_ROOT, userFileDir, fileName), fileName


def scientificinstrumentscalendarpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    context = { 'scientificInstruments': scientificInstruments(), 'bookings': bookings() }
    return render(request, 'pages/scientific_instruments_calendar_page.html', context)

def scientificInstruments():
    scientificInstrumentsAll        = ScientificInstrument.objects.all()
    scientificInstrument            = dict()
    scientificInstrument['all']    = scientificInstrumentsAll.count()
    scientificInstrument['data']    = scientificInstrumentsAll
    return scientificInstrument

def bookings():
    bookingsAll         = Booking.objects.all()
    booking             = dict()
    booking['all']     = bookingsAll.count()
    booking['data']    = bookingsAll
    return booking

def scientificinstrumentslistpage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    scientificInstruments = ScientificInstrument.objects.all().order_by('number')
    if request.method == 'POST':
        nameScientificInstrument    = request.POST['nameScientificInstrument']
        name                        = Q(name__contains=nameScientificInstrument)
        number                      = Q(number__contains=nameScientificInstrument)
        scientificInstruments       = ScientificInstrument.objects.filter(name | number).order_by('name')
    scientificInstrumentsJson = serializers.serialize("json", scientificInstruments)
    context = { 'scientificInstruments': scientificInstruments, 'scientificInstrumentsJson': scientificInstrumentsJson }
    return render(request, 'pages/scientific_instruments_list_page.html', context)

def addscientificinstrumentspage(request):
    if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
        return redirect(reverse('homepage'))
    if request.method == 'POST':
        scientificInstrumentID = request.POST['ScientificInstrumentID']
        scientificInstrument = ScientificInstrument.objects.filter(id=scientificInstrumentID)
        if scientificInstrument.exists():
            context = { 'scientificInstrument': scientificInstrument.first() }
            return render(request, 'pages/add_scientific_instruments.html', context)
        return redirect(reverse('scientific-instruments-list'))
    return render(request, 'pages/add_scientific_instruments.html')