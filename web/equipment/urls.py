# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('edit', views.EditEquipment.as_view(), name='editEquipmentApi'),
    path('add', views.AddEquipment.as_view(), name='addEquipmentApi'),
    path('remove', views.RemoveEquipment.as_view(), name='removeEquipmentApi'),
    path('export/user', views.ExportUserEquipments.as_view(), name='ExportUserEquipments'),
    path('export/order', views.ExportOrderEquipments.as_view(), name='ExportOrderEquipments'),
    path('export/equipments', views.ExportUsesEquipments.as_view(), name='ExportUsesEquipments'),
    
]