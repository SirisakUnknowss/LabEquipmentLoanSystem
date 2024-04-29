# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('add', views.AddItemForBorrowingApi.as_view(), name='addItemForBorrowingApi'),
    path('remove', views.RemoveItemForBorrowingApi.as_view(), name='removeItemForBorrowingApi'),
    path('confirm', views.ConfirmBorrowingApi.as_view(), name='confirmBorrowingApi'),
    path('disapproved', views.DisapprovedBorrowingApi.as_view(), name='disapprovedBorrowingApi'),
    path('approved', views.ApprovedBorrowingApi.as_view(), name='approvedBorrowingApi'),
    path('cancel', views.CancelBorrowingApi.as_view(), name='cancelBorrowingApi'),
    path('delete', views.RemoveBorrowingApi.as_view(), name='removeBorrowingApi'),
    path('returning', views.ReturningApi.as_view(), name='returningApi'),
    path('', views.BorrowAgainApi.as_view(), name='borrowAgainApi'),
    path('confirmreturn', views.ConfirmreturnApi.as_view(), name='confirmreturnApi'),    
]