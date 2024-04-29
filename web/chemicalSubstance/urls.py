# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('edit', views.EditChemicalSubstance.as_view(), name='editChemicalSubstanceApi'),
    path('add', views.AddChemicalSubstance.as_view(), name='addChemicalSubstanceApi'),
    path('remove', views.RemoveChemicalSubstance.as_view(), name='removeChemicalSubstanceApi'),
    path('approval', views.ApprovalChemicalSubstance.as_view(), name='approvalChemicalSubstanceApi'),
    path('cancel', views.CancelChemicalSubstance.as_view(), name='cancelChemicalSubstance'),
    path('withdrawal', views.ConfirmWithdrawalApi.as_view(), name='confirmWithdrawalApi'),
    
]