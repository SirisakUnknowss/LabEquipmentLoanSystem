# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('add', views.AddItemForBorrowingApi.as_view(), name='addItemForBorrowingApi')
]