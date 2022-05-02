# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    # path('register', views.user_register, name='registerApi'),
    path('add', views.AddEquipment.as_view(), name='addEquipmentApi')
]