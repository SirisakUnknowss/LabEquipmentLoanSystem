from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from equipment.models import Equipment

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

def notificationspage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/notifications_page.html')

def informationpage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/information_page.html')

def borrowinghistorypage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/borrowing_history_page.html')

def contactpage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/contact_page.html')

def profilepage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/user_profile.html')

def addequipmentpage(request):
    if not(request.user.account.status == 'admin'):
        return redirect(reverse('homepage'))
    return render(request, 'pages/add_equipment.html')

def equipmentlistpage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    equipments = Equipment.objects.all().values()
    context = { 'equipments': equipments }
    return render(request, 'pages/equipment_list_page.html', context)

def equipmentdetailpage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    if request.method == 'GET':
        return redirect(reverse('equipment-list'))
    equipmentID = request.POST['EquipmentID']
    try:
        equipment = Equipment.objects.get(id=equipmentID)
        context = { 'equipment': equipment }
        return render(request, 'pages/equipment_detail_page.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('equipment-list'))