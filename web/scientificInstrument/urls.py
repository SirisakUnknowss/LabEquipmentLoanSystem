# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('list', views.ListScientificInstrument.as_view(), name='listScientificInstrumentApi'),
    path('edit', views.EditScientificInstrument.as_view(), name='editScientificInstrumentApi'),
    path('add', views.AddScientificInstrument.as_view(), name='addScientificInstrumentApi'),
    path('remove', views.RemoveScientificInstrument.as_view(), name='removeScientificInstrumentApi'),
    path('get/timeStartCanBooking', views.GetTimeStartCanBooking.as_view(), name='GetTimeStartCanBooking'),
    path('get/timeEndCanBooking', views.GetTimeEndCanBooking.as_view(), name='GetTimeEndCanBooking'),
    path('booking', views.BookingScientificInstrumentApi.as_view(), name='BookingScientificInstrumentApi'),
    # path('disapproved', views.DisapprovedBookingApi.as_view(), name='disapprovedBookingApi'),
    # path('approved', views.ApprovedBookingApi.as_view(), name='approvedBookingApi'),
    path('approval', views.ApprovalBookingApi.as_view(), name='approvalBookingApi'),
    path('cancel', views.CancelBookingApi.as_view(), name='cancelBookingApi'),
    path('get', views.GetBookingByID.as_view(), name="GetBookingByID"),
]