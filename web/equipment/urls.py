# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('edit', views.EditEquipment.as_view(), name='editEquipmentApi'),
    path('add', views.AddEquipment.as_view(), name='addEquipmentApi'),
    path('remove', views.RemoveEquipment.as_view(), name='removeEquipmentApi'),
]