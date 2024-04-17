# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('edit', views.EditChemicalSubstance.as_view(), name='editChemicalSubstanceApi'),
    path('add', views.AddChemicalSubstance.as_view(), name='addChemicalSubstanceApi'),
    path('remove', views.RemoveChemicalSubstance.as_view(), name='removeChemicalSubstanceApi'),
]