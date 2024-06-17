# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('edit', views.EditChemicalSubstance.as_view(), name='editChemicalSubstanceApi'),
    path('add', views.AddChemicalSubstance.as_view(), name='addChemicalSubstanceApi'),
    path('approval', views.ApprovalChemicalSubstance.as_view(), name='approvalChemicalSubstanceApi'),
    path('cancel', views.CancelChemicalSubstance.as_view(), name='cancelChemicalSubstance'),
    path('withdrawal', views.ConfirmWithdrawalApi.as_view(), name='confirmWithdrawalApi'),
    path('cart/add', views.AddToCartView.as_view(), name='addToCartAPI'),
    path('cart/remove', views.RemoveFromCartView.as_view(), name='removeFromCartAPI'),
    path('export/user', views.ExportUserChemicalSubstances.as_view(), name='ExportUserChemicalSubstances'),
    path('export/order', views.ExportOrderChemicalSubstances.as_view(), name='ExportOrderChemicalSubstances'),
    path('export/chemicalSubstances', views.ExportUsesChemicalSubstances.as_view(), name='ExportUsesChemicalSubstances'),
]