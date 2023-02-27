# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('edit', views.EditScientificInstrument.as_view(), name='editScientificInstrumentApi'),
    path('add', views.AddScientificInstrument.as_view(), name='addScientificInstrumentApi'),
    path('remove', views.RemoveScientificInstrument.as_view(), name='removeScientificInstrumentApi'),
    path('get/timeCanBooking', views.GetTimeCanBooking.as_view(), name='GetTimeCanBooking'),
    path('booking', views.BookingScientificInstrumentApi.as_view(), name='BookingScientificInstrumentApi'),
    path('disapproved', views.DisapprovedBookingApi.as_view(), name='disapprovedBookingApi'),
    path('approved', views.ApprovedBookingApi.as_view(), name='approvedBookingApi'),
    path('cancel', views.CancelBookingApi.as_view(), name='cancelBookingApi'),
]