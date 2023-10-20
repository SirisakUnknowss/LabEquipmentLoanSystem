# Python
import os
from datetime import datetime
# Django
from django.db.models import Q
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from django.urls import reverse
#Project
from account.models import Account
from account.admin import AccountResource
from base.models import DataWeb
from base.functions import download_file, getDataFile
from borrowing.admin import OrderModelResource
from borrowing.models import EquipmentCart, Order
from equipment.admin import EquipmentModelResource
from equipment.models import Equipment
from scientificInstrument.models import ScientificInstrument, Booking
from scientificInstrument.admin import BookingModelResource, ScientificInstrumentModelResource
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

def registerPage(request):
    if  request.method == 'POST' and request.POST['accountID']:
        account = Account.objects.get(id=request.POST['accountID'])
        context = { 'account': account }
        return render(request, 'base/signup.html', context)
    return render(request, 'base/signup.html')

def equipmentLandingPage(request):
    if not(request.user.is_authenticated):
        return render(request, 'base/login.html')
    checkOverDued(request)
    return render(request, 'pages/equipments/index.html')

def notificationsEquipmentPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    account = request.user.account
    checkOverDued(request)
    orders      = getOrders(account)
    context     = { 'orders': orders }
    return render(request, 'pages/equipments/notifications_page.html', context)

def getOrders(account: Account):
    orders = Order.objects.filter(user=account, status=Order.STATUS.OVERDUED)
    if account.status == Account.STATUS.ADMIN:
        returned    = Q(status=Order.STATUS.RETURNED)
        waiting     = Q(status=Order.STATUS.WAITING)
        overdued    = Q(status=Order.STATUS.OVERDUED)
        orders      = Order.objects.filter(waiting | returned | overdued)
    return orders

def getBookings(account: Account):
    waiting     = Q(status=Order.STATUS.WAITING)
    approved    = Q(status=Order.STATUS.APPROVED)
    bookings = Booking.objects.filter(user=account).filter(approved | waiting)
    if account.status == Account.STATUS.ADMIN:
        waiting     = Q(status=Order.STATUS.WAITING)
        bookings      = Booking.objects.filter(waiting)
    return bookings

def informationEquipmentPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    waiting     = Q(status=Order.STATUS.WAITING)
    approved    = Q(status=Order.STATUS.APPROVED)
    returned    = Q(status=Order.STATUS.RETURNED)
    orders      = Order.objects.filter(waiting | approved | returned)
    if request.user.account.status == Account.STATUS.USER:
        orders  = orders.filter(user=request.user.account)
    context     = { 'orders': orders }
    return render(request, 'pages/equipments/information_page.html', context)

def borrowingHistoryPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    canceled    = Q(status=Order.STATUS.CANCELED)
    completed   = Q(status=Order.STATUS.COMPLETED)
    disapproved = Q(status=Order.STATUS.DISAPPROVED)
    orders      = Order.objects.filter(disapproved | canceled | completed)
    if request.user.account.status == Account.STATUS.USER:
        orders  = orders.filter(user=request.user.account)
    context     = { 'orders': orders }
    return render(request, 'pages/equipments/borrowing_history_page.html', context)

def analysisPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    context = { 'orders': orderAll(), 'accounts': accountAll(), 'equipments': topEquipment() }
    return render(request, 'pages/equipments/analysisPage.html', context)

def topEquipment():
    equipments = Equipment.objects.all().order_by('-statistics').filter(statistics__gt=1)[:20]
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
    overDued    = Q(status=Order.STATUS.OVERDUED)
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
    order['overdued']       = orders.filter(overDued).count()
    order['completed']      = orders.filter(completed).count()
    order['disapproved']    = orders.filter(disapproved).count()
    return order


def contactPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    dataWeb = DataWeb.objects.all().first()
    context = { 'dataWeb': dataWeb }
    return render(request, 'pages/contact_page.html', context)

def profilePage(request):
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

def addEquipmentPage(request):
    if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
        return redirect(reverse('homepage'))
    if request.method == 'POST':
        equipmentID = request.POST['EquipmentID']
        equipment = Equipment.objects.filter(id=equipmentID)
        if equipment.exists():
            context = { 'equipment': equipment.first() }
            return render(request, 'pages/equipments/add_equipment.html', context)
        return redirect(reverse('equipmentListPage'))
    return render(request, 'pages/equipments/add_equipment.html')

def equipmentListPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    equipments = Equipment.objects.all().order_by('name')
    if request.method == 'POST':
        nameEquipment   = request.POST['nameequipment']
        name            = Q(name__contains=nameEquipment)
        equipments      = Equipment.objects.filter(name).order_by('name')
    equipmentsJson = serializers.serialize("json", equipments)
    context = { 'equipments': equipments, 'equipmentsJson': equipmentsJson }
    return render(request, 'pages/equipments/equipment_list_page.html', context)

def detailEquipmentPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    if request.method == 'GET':
        return redirect(reverse('homepage'))
    status      = request.POST['StatusBorrowing']
    equipmentID = request.POST['EquipmentID']
    try:
        order   = Order.objects.get(id=equipmentID, status=status)
        context = { 'order': order, 'status': status }
        return render(request, 'pages/equipments/equipment_detail_page.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('equipmentListPage'))

def equipmentCartListPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    equipmentsCart = EquipmentCart.objects.filter(user=request.user.account)
    context = { 'equipmentsCart': equipmentsCart }
    return render(request, 'pages/equipments/cart_equipment_page.html', context)

def userManagementPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    return render(request, 'pages/user_management_page.html')

def userEditPage(request):
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
        filePath, fileName = self.writeFile()
        return download_file(filePath, fileName)

    def writeFile(self):
        userFileDir = "UserData"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        fileName = "userData"
        
        xlsxFile = getDataFile(dirPath, fileName, AccountResource)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportBorrowingData(LabAPIView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        return download_file(filePath, fileName)

    def writeFile(self, parameter_value):
        userFileDir = "OrderData"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = Order.objects.filter(status=parameter_value)
        fileName = f"{parameter_value}Data"
        if parameter_value == "":
            queryset = Order.objects.all()
            fileName = "allData"
        
        xlsxFile = getDataFile(dirPath, fileName, OrderModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportEquipments(LabAPIView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        return download_file(filePath, fileName)

    def writeFile(self, parameter_value):
        userFileDir = "Equipments"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = Equipment.objects.all()
        if parameter_value != "":
            queryset = Equipment.objects.all().order_by('-statistics').filter(statistics__gt=1)
        fileName = f"Equipments{parameter_value}Data"
        
        xlsxFile = getDataFile(dirPath, fileName, EquipmentModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

def scientificInstrumentLandingPage(request):
    if not(request.user.is_authenticated):
        return render(request, 'base/login.html')
    checkOverDued(request)
    return render(request, 'pages/scientificInstruments/index.html')

def scientificInstrumentsCalendarPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    scientificInstrumentID = None
    if request.method == "POST":
        scientificInstrumentID = request.POST["scientificInstrumentID"]
    checkOverDued(request)
    context = { 'scientificInstruments': scientificInstruments(), 'bookings': bookings(scientificInstrumentID), 'scientificInstrumentID':scientificInstrumentID }
    return render(request, 'pages/scientificInstruments/calendarPage.html', context)

def scientificInstruments():
    scientificInstrumentsAll        = ScientificInstrument.objects.all()
    scientificInstrument            = dict()
    scientificInstrument['all']     = scientificInstrumentsAll.count()
    scientificInstrument['data']    = scientificInstrumentsAll
    return scientificInstrument

def bookings(idScientificInstrument):
    try:
        scientificInstrument    = ScientificInstrument.objects.get(pk=int(idScientificInstrument))
        bookingsAll             = Booking.objects.filter(scientificInstrument=scientificInstrument).order_by('-dateBooking', '-timeBooking')
    except:
        bookingsAll = Booking.objects.all().order_by('-dateBooking', '-timeBooking')
    booking         = dict()
    booking['all']  = bookingsAll.count()
    booking['data'] = getBookingList(bookingsAll)
    return booking

def getBookingList(bookingsAll):
    bookingList = []
    for booking in bookingsAll:
        booking: Booking = booking
        day ="{:02d}".format(booking.dateBooking.day)
        month = "{:02d}".format(booking.dateBooking.month)
        year = booking.dateBooking.year
        jsonData = {}
        jsonData["title"] = f"{booking.scientificInstrument.name}"
        jsonData["start"] = f"{year}-{month}-{day}"
        jsonData["url"] = booking.pk
        bookingList.append(jsonData)
    return (str(bookingList)).replace("\'", "\"")

def scientificInstrumentsListPage(request):
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
    return render(request, 'pages/scientificInstruments/listPage.html', context)

def addScientificInstrumentPage(request):
    if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
        return redirect(reverse('homepage'))
    if request.method == 'POST':
        scientificInstrumentID = request.POST['ScientificInstrumentID']
        scientificInstrument = ScientificInstrument.objects.filter(id=scientificInstrumentID)
        if scientificInstrument.exists():
            context = { 'scientificInstrument': scientificInstrument.first() }
            return render(request, 'pages/scientificInstruments/add_scientific_instruments.html', context)
        return redirect(reverse('scientificInstrumentsListPage'))
    return render(request, 'pages/scientificInstruments/add_scientific_instruments.html')

def informationBookingPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    waiting     = Q(status=Order.STATUS.WAITING)
    approved    = Q(status=Order.STATUS.APPROVED)
    bookings    = Booking.objects.filter(waiting | approved)
    if request.user.account.status == Account.STATUS.USER:
        bookings  = bookings.filter(user=request.user.account)
    context     = { 'bookings': bookings.order_by('-dateBooking', '-timeBooking') }
    return render(request, 'pages/scientificInstruments/informationPage.html', context)

def detailScientificInstrumentPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    checkOverDued(request)
    if request.method == 'GET':
        return redirect(reverse('homepage'))
    status      = request.POST['StatusBooking']
    bookingID   = request.POST['bookingID']
    try:
        booking   = Booking.objects.get(id=bookingID, status=status)
        context = { 'booking': booking, 'status': status }
        return render(request, 'pages/scientificInstruments/detail_page.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('informationBookingPage'))

def notificationBookingPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    account = request.user.account
    checkOverDued(request)
    bookings    = getBookings(account)
    context     = {'bookings': bookings.order_by('-dateBooking', '-timeBooking') }
    return render(request, 'pages/scientificInstruments/notificationPage.html', context)


def analysisScientificInstrumentPage(request):
    if not(request.user.is_authenticated): return redirect(reverse('homepage'))
    context = { 'bookings': bookingAll(), 'scientificInstruments': topScientificInstrument() }
    return render(request, 'pages/scientificInstruments/analysisPage.html', context)

def topScientificInstrument():
    scientificInstruments = ScientificInstrument.objects.all().order_by('-statistics').filter(statistics__gt=1)[:20]
    return scientificInstruments

def bookingAll():
    waiting     = Q(status=Order.STATUS.WAITING)
    approved    = Q(status=Order.STATUS.APPROVED)
    canceled    = Q(status=Order.STATUS.CANCELED)
    disapproved = Q(status=Order.STATUS.DISAPPROVED)
    order       = dict()
    bookings    = Booking.objects.all()

    order['all']            = bookings.count()
    order['waiting']        = bookings.filter(waiting).count()
    order['canceled']       = bookings.filter(canceled).count()
    order['approved']       = bookings.filter(approved).count()
    order['disapproved']    = bookings.filter(disapproved).count()
    return order

class ExportScientificInstruments(LabAPIView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        return download_file(filePath, fileName)

    def writeFile(self, parameter_value):
        userFileDir = "ScientificInstruments"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = ScientificInstrument.objects.all()
        if parameter_value != "":
            queryset = ScientificInstrument.objects.all().order_by('-statistics').filter(statistics__gt=1)
        fileName = f"Equipments{parameter_value}Data"
        
        xlsxFile = getDataFile(dirPath, fileName, ScientificInstrumentModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportBookingData(LabAPIView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        parameter_value     = request.GET['getData']
        filePath, fileName  = self.writeFile(parameter_value)
        return download_file(filePath, fileName)

    def writeFile(self, parameter_value):
        userFileDir = "BookingData"
        dirPath     = f"{MEDIA_ROOT}/files/{userFileDir}"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        queryset    = Booking.objects.filter(status=parameter_value)
        fileName    = f"{parameter_value}Data"
        if parameter_value == "":
            queryset = Booking.objects.all()
            fileName = "allData"
        
        xlsxFile = getDataFile(dirPath, fileName, BookingModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile