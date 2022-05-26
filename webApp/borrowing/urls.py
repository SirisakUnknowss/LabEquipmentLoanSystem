# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('add', views.AddItemForBorrowingApi.as_view(), name='addItemForBorrowingApi'),
    path('remove', views.RemoveItemForBorrowingApi.as_view(), name='removeItemForBorrowingApi'),
    path('confirm', views.ConfirmBorringApi.as_view(), name='confirmBorringApi'),
    
]