# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('add', views.AddItemForBorrowingApi.as_view(), name='addItemForBorrowingApi'),
    path('remove', views.RemoveItemForBorrowingApi.as_view(), name='removeItemForBorrowingApi'),
    path('confirm', views.ConfirmBorringApi.as_view(), name='confirmBorringApi'),
    path('disapproved', views.DisapprovedBorringApi.as_view(), name='disapprovedBorringApi'),
    path('approved', views.ApprovedBorringApi.as_view(), name='approvedBorringApi'),
    path('cancel', views.CancelBorringApi.as_view(), name='cancelBorringApi'),
    path('delete', views.RemoveBorringApi.as_view(), name='removeBorringApi'),    
    
]