from django.shortcuts import render

from base.views import LabListView
from .models import Equipment
from rest_framework.permissions import AllowAny

# Create your views here.
class ListEquipment(LabListView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzPrototypeRobot
    permission_classes = [ AllowAny ]