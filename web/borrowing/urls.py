# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('add', views.AddItemForBorrowingApi.as_view(), name='addItemForBorrowingApi'),
    path('remove', views.RemoveItemForBorrowingApi.as_view(), name='removeItemForBorrowingApi'),
    path('confirm', views.ConfirmBorrowingApi.as_view(), name='confirmBorrowingApi'),
    path('approved', views.ApprovalBorrowingApi.as_view(), name='approvalBorrowingApi'),
    path('cancel', views.CancelBorrowingApi.as_view(), name='cancelBorrowingApi'),
    path('delete', views.RemoveBorrowingApi.as_view(), name='removeBorrowingApi'),
    path('returning', views.ReturnEquipmentsApi.as_view(), name='returnEquipmentsApi'),
    path('again', views.BorrowingAgainApi.as_view(), name='borrowingAgainApi'),
    path('return/confirm', views.ConfirmReturnApi.as_view(), name='confirmReturnApi'),    
]