# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('edit', views.EditScientificInstrument.as_view(), name='editScientificInstrumentApi'),
    path('add', views.AddScientificInstrument.as_view(), name='addScientificInstrumentApi'),
    path('remove', views.RemoveScientificInstrument.as_view(), name='removeScientificInstrumentApi'),
]