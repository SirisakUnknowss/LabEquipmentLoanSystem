# Django
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

#Project
from equipment.models import Equipment
from borrowing.models import EquipmentCart, Order

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

# Create your views here.
def homepage(request):
    if not(request.user.is_authenticated):
        return render(request, 'base/login.html')
    return render(request, 'base/index.html')

def registerpage(request):
    return render(request, 'base/signup.html')

def check_login(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))

def notificationspage(request):
    check_login(request)
    orders = Order.objects.filter(user=request.user.account, status=Order.STATUS.OVERDUED)
    context = { 'orders': orders }
    return render(request, 'pages/notifications_page.html', context)

def informationpage(request):
    check_login(request)
    orders = Order.objects.filter(user=request.user.account).exclude(status=Order.STATUS.CANCELLED)
    context = { 'orders': orders }
    return render(request, 'pages/information_page.html', context)

def borrowinghistorypage(request):
    check_login(request)
    return render(request, 'pages/borrowing_history_page.html')

def contactpage(request):
    check_login(request)
    return render(request, 'pages/contact_page.html')

def profilepage(request):
    check_login(request)
    return render(request, 'pages/user_profile.html')

def addequipmentpage(request):
    check_login(request)
    return render(request, 'pages/add_equipment.html')

def equipmentlistpage(request):
    check_login(request)
    equipments = Equipment.objects.all().values()
    context = { 'equipments': equipments }
    return render(request, 'pages/equipment_list_page.html', context)

def equipmentdetailpage(request):
    check_login(request)
    if request.method == 'GET':
        return redirect(reverse('equipment-list'))
    equipmentID = request.POST['EquipmentID']
    try:
        equipment = Equipment.objects.get(id=equipmentID)
        context = { 'equipment': equipment }
        return render(request, 'pages/equipment_detail_page.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('equipment-list'))

def equipmentcartlistpage(request):
    check_login(request)
    equipmentsCart = EquipmentCart.objects.filter(user=request.user.account)
    context = { 'equipmentsCart': equipmentsCart }
    return render(request, 'pages/cart_equipment_page.html', context)