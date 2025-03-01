# Python
import os
# Django
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
#Project
from account.admin import AccountResource
from account.models import Account
from base.functions import downloadFile, getDataFile
from base.menu import MenuList, AdminOnly
from base.models import DataWeb
from base.permissions import IsAdminAccount
from base.variables import addVariables
from borrowing.admin import OrderModelResource
from borrowing.models import Order
from chemicalSubstance.admin import ChemicalSubstanceModelResource
from chemicalSubstance.models import ChemicalSubstance
from equipment.admin import EquipmentModelResource
from equipment.models import Equipment
from scientificInstrument.admin import BookingModelResource, ScientificInstrumentModelResource
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

# ==================================== MAIN PAGE ==================================== #

class LandingView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.setMenuHome()
        self.context['menuUpList'][0]['active'] = True
        return render(request, 'base/index.html', self.context)

class NotFoundPageView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'error/404.html')

    def post(self, request, *args, **kwargs):
        return render(request, 'error/404.html')

class SignupView(View):

    def get(self, request, *args, **kwargs):
        self.context = {}
        self.context['titlePage'] = 'ลงทะเบียนเข้าใช้งาน'
        self.context = addVariables(self.context)
        if request.user.is_authenticated:
            return redirect(reverse('homepage'))
        return render(request, 'base/signup.html', self.context)

class AddUserView(AdminOnly):

    def get(self, request, *args, **kwargs):
        self.context['titlePage']   = 'เพิ่มผู้ใช้งาน'
        self.context['adduser']     = True
        self.context = addVariables(self.context)
        if request.user.is_authenticated and request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        return render(request, 'base/signup.html', self.context)

class ContactView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        dataWeb = DataWeb.objects.all().first()
        self.setMenuHome()
        self.context['menuDownList'][0]['active'] = True
        self.context['dataWeb'] = dataWeb
        return render(request, 'pages/contactPage.html', self.context)

class ProfileView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.setMenuHome()
        self.context['titleBar'] = "ข้อมูลบัญชีผู้ใช้งาน"
        return render(request, 'pages/userProfile.html', self.context)

class EditProfileView(View):
    
    def get(self, request: Request, *args, **kwargs):
        return redirect(reverse('homepage'))

    def post(self, request: Request, *args, **kwargs):
        self.context    = {}
        self.linkBack   = '/account/profile'
        if not request.user.is_authenticated:
            return redirect(reverse('homepage'))
        status = request.user.account.status
        if 'accountID' in request.POST and status == Account.STATUS.ADMIN:
            account                 = request.POST['accountID']
            self.linkBack           = '/user/list'
            self.account: Account   = Account.objects.get(id=account)
        else:
            self.account = request.user.account
        self.getData()
        return render(request, 'base/signup.html', self.context)

    def getData(self):
            branch = f'{self.account.faculty}_{self.account.branch}'
            if self.account.faculty == 'other':
                branch = 'other'
            self.context['branch']      =  branch
            self.context['account']     = self.account
            self.context['titlePage']   = 'แก้ไขข้อมูลส่วนตัว'
            self.context['linkBack']    = self.linkBack
            self.context = addVariables(self.context)
        

class UserManagementView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        self.setMenuHome()
        self.context['menuDownList'][1]['active'] = True
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        return render(request, 'pages/userManagementPage.html', self.context)

class UserListPageView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        self.setMenuHome()
        self.context['menuDownList'][1]['active'] = True
        self.context['accounts'] = Account.objects.all().order_by('id')
        return render(request, 'pages/manageUserPage.html', self.context)

    def post(self, request, *args, **kwargs):
        super(MenuList, self).post(request)
        status      = request.POST['status']
        username    = request.POST['username']
        studentID   = Q(studentID__contains=username)
        firstname   = Q(firstname__contains=username)
        lastname    = Q(lastname__contains=username)
        branch      = Q(branch__contains=username)
        accounts    = Account.objects.filter(studentID | firstname | lastname | branch).order_by('id')
        self.context['accounts'] = 'notfound'
        self.context['status'] = ''
        if accounts.exists():
            self.context['accounts'] = accounts
            self.context['status'] = 'view'
            if status == 'edit':
                self.context['status'] = 'edit'
        return render(request, 'pages/manageUserPage.html', self.context)

# ==================================== MAIN PAGE ==================================== #


# ==================================== EXPORT DATA ==================================== #

class ExportUserData(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request, *args, **kwargs):
        filePath, fileName = self.writeFile()
        return downloadFile(filePath, fileName)

    def writeFile(self):
        userFileDir = "UserData"
        dirPath     = f"{MEDIA_ROOT}/files/{userFileDir}"
        fileName    = "userData"
        queryset    = Account.objects.all()
        xlsxFile    = getDataFile(dirPath, fileName, AccountResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportBorrowingData(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        return downloadFile(filePath, fileName)

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
    permission_classes = [ IsAdminAccount ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        return downloadFile(filePath, fileName)

    def writeFile(self, parameter_value):
        userFileDir = "Equipments"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = Equipment.objects.all()
        if parameter_value != "":
            queryset = Equipment.objects.all().order_by('-statistics').filter(statistics__gte=1)
        fileName = f"Equipments{parameter_value}Data"
        
        xlsxFile = getDataFile(dirPath, fileName, EquipmentModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportScientificInstruments(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        return downloadFile(filePath, fileName)

    def writeFile(self, parameter_value):
        userFileDir = "ScientificInstruments"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = ScientificInstrument.objects.all()
        if parameter_value != "":
            queryset = ScientificInstrument.objects.all().order_by('-statistics').filter(statistics__gte=1)
        fileName = f"ScientificInstruments{parameter_value}Data"
        
        xlsxFile = getDataFile(dirPath, fileName, ScientificInstrumentModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportChemicalSubstances(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request, *args, **kwargs):
        parameter_value = request.GET['getData']
        filePath, fileName = self.writeFile(parameter_value)
        return downloadFile(filePath, fileName)

    def writeFile(self, parameter_value):
        userFileDir = "ChemicalSubstances"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = ChemicalSubstance.objects.all()
        if parameter_value != "":
            queryset = ChemicalSubstance.objects.all().order_by('-statistics').filter(statistics__gte=1)
        fileName = f"ChemicalSubstances{parameter_value}Data"
        
        xlsxFile = getDataFile(dirPath, fileName, ChemicalSubstanceModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportBookingData(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request, *args, **kwargs):
        parameter_value     = request.GET['getData']
        filePath, fileName  = self.writeFile(parameter_value)
        return downloadFile(filePath, fileName)

    def writeFile(self, parameter_value):
        userFileDir = "BookingData"
        dirPath     = f"{MEDIA_ROOT}/files/{userFileDir}"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        queryset    = Booking.objects.filter(status=parameter_value).order_by('dateBooking')
        fileName    = f"{parameter_value}Data"
        if parameter_value == "":
            queryset = Booking.objects.all().order_by('dateBooking')
            fileName = "allData"
        xlsxFile = getDataFile(dirPath, fileName, BookingModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

# ==================================== EXPORT DATA ==================================== #