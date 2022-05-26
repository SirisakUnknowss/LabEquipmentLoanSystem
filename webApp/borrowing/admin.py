from django.contrib import admin
from .models import EquipmentCart, Borrowing, Order
from import_export.admin import ImportExportModelAdmin


@admin.register(EquipmentCart)
class EquipmentCartAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'user', 'quantity', 'equipment' ]

@admin.register(Borrowing)
class BorrowingAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'user', 'quantity', 'equipment' ]

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'user', 'quantity', 'dateBorrowing', 'dateReturn', 'approver', 'status' ]